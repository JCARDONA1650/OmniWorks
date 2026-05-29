from django.db import models
from django.conf import settings


class NoteCategory(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='note_categories'
    )
    name = models.CharField(max_length=60)
    color = models.CharField(max_length=7, default='#1e6fff')

    class Meta:
        db_table = 'note_categories'
        ordering = ['name']
        unique_together = ('user', 'name')
        verbose_name = 'Categoría de nota'
        verbose_name_plural = 'Categorías de notas'

    def __str__(self):
        return f'{self.name} ({self.user.email})'


class Note(models.Model):
    class NoteType(models.TextChoices):
        QUICK = 'quick', 'Nota rápida'
        REPORT = 'report', 'Informe'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notes'
    )
    category = models.ForeignKey(
        NoteCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='notes'
    )
    title = models.CharField(max_length=200, blank=True, default='Sin título')
    content = models.TextField(blank=True, default='')
    note_type = models.CharField(max_length=10, choices=NoteType.choices, default=NoteType.QUICK)
    is_pinned = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    has_offensive_content = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'notes'
        ordering = ['-is_pinned', '-updated_at']
        verbose_name = 'Nota'
        verbose_name_plural = 'Notas'

    def __str__(self):
        return f'{self.title} — {self.user.email}'


class NoteAIResult(models.Model):
    class Action(models.TextChoices):
        SUMMARIZE  = 'summarize',  'Resumen'
        IMPROVE    = 'improve',    'Mejorar redacción'
        REPORT     = 'report',     'Convertir a informe'
        TASKS      = 'tasks',      'Extraer tareas'
        KEY_POINTS = 'key_points', 'Puntos clave'
        MEETING    = 'meeting',    'Acta de reunión'

    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='ai_results')
    action = models.CharField(max_length=20, choices=Action.choices)
    original_content = models.TextField()
    processed_content = models.TextField()
    tokens_used = models.PositiveIntegerField(default=0)
    provider = models.CharField(max_length=30, default='claude')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'note_ai_results'
        ordering = ['-created_at']
        verbose_name = 'Resultado IA'
        verbose_name_plural = 'Resultados IA'

    def __str__(self):
        return f'{self.get_action_display()} — {self.note.title}'


class NoteHistory(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='history')
    title = models.CharField(max_length=200, blank=True)
    content = models.TextField(blank=True)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'note_history'
        ordering = ['-saved_at']
        verbose_name = 'Historial de nota'
        verbose_name_plural = 'Historial de notas'

    def __str__(self):
        return f'Historial #{self.pk} — {self.note.title}'
