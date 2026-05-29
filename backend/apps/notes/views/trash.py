from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.notes.models import Note
from apps.notes.serializers import NoteListSerializer


class NoteTrashView(generics.ListAPIView):
    serializer_class = NoteListSerializer

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user, is_deleted=True)


class NoteRestoreView(APIView):
    def post(self, request, pk):
        note = Note.objects.filter(pk=pk, user=request.user, is_deleted=True).first()
        if not note:
            return Response({'detail': 'Nota no encontrada en papelera.'}, status=status.HTTP_404_NOT_FOUND)
        note.is_deleted = False
        note.save()
        return Response({'detail': 'Nota restaurada correctamente.'})
