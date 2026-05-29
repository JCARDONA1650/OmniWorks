from rest_framework import generics
from apps.notes.models import NoteCategory
from apps.notes.serializers import NoteCategorySerializer


class NoteCategoryListCreateView(generics.ListCreateAPIView):
    serializer_class = NoteCategorySerializer

    def get_queryset(self):
        return NoteCategory.objects.filter(user=self.request.user)


class NoteCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NoteCategorySerializer

    def get_queryset(self):
        return NoteCategory.objects.filter(user=self.request.user)
