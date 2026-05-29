from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.notes.models import Note, NoteHistory
from apps.notes.serializers import NoteSerializer, NoteHistorySerializer


class NoteHistoryView(generics.ListAPIView):
    serializer_class = NoteHistorySerializer

    def get_queryset(self):
        note = Note.objects.filter(
            pk=self.kwargs['pk'], user=self.request.user, is_deleted=False
        ).first()
        return NoteHistory.objects.filter(note=note) if note else NoteHistory.objects.none()


class NoteRestoreHistoryView(APIView):
    def post(self, request, pk, history_pk):
        note = Note.objects.filter(pk=pk, user=request.user, is_deleted=False).first()
        if not note:
            return Response({'detail': 'Nota no encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        history = NoteHistory.objects.filter(pk=history_pk, note=note).first()
        if not history:
            return Response({'detail': 'Versión no encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        NoteHistory.objects.create(note=note, title=note.title, content=note.content)
        note.title = history.title
        note.content = history.content
        note.save()
        return Response(NoteSerializer(note).data)
