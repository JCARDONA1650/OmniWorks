from django.contrib import admin
from .models import Note, NoteCategory, NoteHistory


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'note_type', 'is_pinned', 'has_offensive_content', 'is_deleted', 'updated_at')
    list_filter = ('note_type', 'is_pinned', 'is_deleted', 'has_offensive_content')
    search_fields = ('title', 'content', 'user__email')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(NoteCategory)
class NoteCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'user')
    search_fields = ('name', 'user__email')


@admin.register(NoteHistory)
class NoteHistoryAdmin(admin.ModelAdmin):
    list_display = ('note', 'saved_at')
    readonly_fields = ('saved_at',)
