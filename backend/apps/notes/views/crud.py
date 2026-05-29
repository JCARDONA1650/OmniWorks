from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q

from apps.notes.models import Note, NoteHistory
from apps.notes.serializers import (
    NoteListSerializer, NoteSerializer,
    NoteCreateSerializer, NoteUpdateSerializer,
)


class NoteListCreateView(generics.ListCreateAPIView):

    def get_queryset(self):
        qs = Note.objects.filter(user=self.request.user, is_deleted=False)
        p = self.request.query_params
        if p.get('search'):
            qs = qs.filter(Q(title__icontains=p['search']) | Q(content__icontains=p['search']))
        if p.get('type') in ('quick', 'report'):
            qs = qs.filter(note_type=p['type'])
        if p.get('category'):
            qs = qs.filter(category_id=p['category'])
        if p.get('pinned') == 'true':
            qs = qs.filter(is_pinned=True)
        return qs

    def get_serializer_class(self):
        return NoteCreateSerializer if self.request.method == 'POST' else NoteListSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        note = serializer.save(user=request.user)
        return Response(NoteSerializer(note).data, status=status.HTTP_201_CREATED)


class NoteDetailView(generics.RetrieveUpdateDestroyAPIView):

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user, is_deleted=False)

    def get_serializer_class(self):
        return NoteUpdateSerializer if self.request.method in ('PUT', 'PATCH') else NoteSerializer

    def perform_update(self, serializer):
        note = self.get_object()
        if note.content or note.title:
            NoteHistory.objects.create(note=note, title=note.title, content=note.content)
            old = NoteHistory.objects.filter(note=note).order_by('-saved_at')[20:]
            NoteHistory.objects.filter(pk__in=old).delete()
        serializer.save()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(NoteSerializer(instance).data)

    def destroy(self, request, *args, **kwargs):
        note = self.get_object()
        note.is_deleted = True
        note.save()
        return Response({'detail': 'Nota eliminada correctamente.'})


class NoteTogglePinView(APIView):
    def post(self, request, pk):
        note = Note.objects.filter(pk=pk, user=request.user, is_deleted=False).first()
        if not note:
            return Response({'detail': 'Nota no encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        note.is_pinned = not note.is_pinned
        note.save()
        return Response({'is_pinned': note.is_pinned})
