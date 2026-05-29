from django.urls import path
from apps.notes.views import (
    NoteCategoryListCreateView, NoteCategoryDetailView,
    NoteListCreateView, NoteDetailView, NoteTogglePinView,
    NoteHistoryView, NoteRestoreHistoryView,
    NoteTrashView, NoteRestoreView,
    NoteAIProcessView, NoteAIHistoryView,
)

urlpatterns = [
    # Categorías
    path('notes/categories/',         NoteCategoryListCreateView.as_view(), name='note_categories'),
    path('notes/categories/<int:pk>/', NoteCategoryDetailView.as_view(),    name='note_category_detail'),

    # Papelera (antes que <int:pk> para que no colisione)
    path('notes/trash/',              NoteTrashView.as_view(),     name='note_trash'),

    # CRUD
    path('notes/',                    NoteListCreateView.as_view(),  name='note_list'),
    path('notes/<int:pk>/',           NoteDetailView.as_view(),      name='note_detail'),
    path('notes/<int:pk>/pin/',       NoteTogglePinView.as_view(),   name='note_pin'),

    # Historial
    path('notes/<int:pk>/history/',                              NoteHistoryView.as_view(),        name='note_history'),
    path('notes/<int:pk>/history/<int:history_pk>/restore/',     NoteRestoreHistoryView.as_view(), name='note_restore_history'),

    # Restaurar desde papelera
    path('notes/<int:pk>/restore/',   NoteRestoreView.as_view(),     name='note_restore'),

    # IA Empresarial
    path('notes/<int:pk>/ai/',        NoteAIHistoryView.as_view(),   name='note_ai_history'),
    path('notes/<int:pk>/ai/process/',NoteAIProcessView.as_view(),   name='note_ai_process'),
]
