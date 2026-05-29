from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.serializers import ModelSerializer

from apps.notes.models import Note, NoteAIResult
from apps.notes.ai_service import process_with_ai, AIAction


class NoteAIResultSerializer(ModelSerializer):
    action_display = None

    class Meta:
        model = NoteAIResult
        fields = ['id', 'action', 'original_content', 'processed_content',
                  'tokens_used', 'provider', 'created_at']


class NoteAIProcessView(APIView):
    """Procesa el contenido de una nota con IA y guarda el resultado."""

    def post(self, request, pk):
        note = Note.objects.filter(pk=pk, user=request.user, is_deleted=False).first()
        if not note:
            return Response({'detail': 'Nota no encontrada.'}, status=status.HTTP_404_NOT_FOUND)

        action_str = request.data.get('action', 'improve')
        try:
            action = AIAction(action_str)
        except ValueError:
            return Response(
                {'detail': f'Acción inválida. Opciones: {[a.value for a in AIAction]}'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        content = note.content
        if not content.strip():
            return Response({'detail': 'La nota no tiene contenido para procesar.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            result = process_with_ai(content, action, title=note.title)
        except ValueError as e:
            return Response({'detail': str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except Exception as e:
            return Response({'detail': f'Error al procesar con IA: {str(e)}'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        ai_result = NoteAIResult.objects.create(
            note=note,
            action=action.value,
            original_content=content,
            processed_content=result.processed,
            tokens_used=result.tokens_used,
            provider=result.provider,
        )
        return Response(NoteAIResultSerializer(ai_result).data, status=status.HTTP_201_CREATED)


class NoteAIHistoryView(generics.ListAPIView):
    """Listado de todos los resultados IA de una nota."""
    serializer_class = NoteAIResultSerializer

    def get_queryset(self):
        note = Note.objects.filter(
            pk=self.kwargs['pk'], user=self.request.user, is_deleted=False
        ).first()
        return NoteAIResult.objects.filter(note=note) if note else NoteAIResult.objects.none()
