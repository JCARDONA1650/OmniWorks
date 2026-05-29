from rest_framework import serializers
from .models import Note, NoteCategory, NoteHistory
from .offensive import contains_offensive_content


class NoteCategorySerializer(serializers.ModelSerializer):
    notes_count = serializers.SerializerMethodField()

    class Meta:
        model = NoteCategory
        fields = ['id', 'name', 'color', 'notes_count']
        read_only_fields = ['id']

    def get_notes_count(self, obj):
        return obj.notes.filter(is_deleted=False).count()

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class NoteHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NoteHistory
        fields = ['id', 'title', 'content', 'saved_at']


class NoteSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()
    category_color = serializers.SerializerMethodField()

    class Meta:
        model = Note
        fields = [
            'id', 'title', 'content', 'note_type',
            'category', 'category_name', 'category_color',
            'is_pinned', 'has_offensive_content',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'has_offensive_content', 'created_at', 'updated_at']

    def get_category_name(self, obj):
        return obj.category.name if obj.category else None

    def get_category_color(self, obj):
        return obj.category.color if obj.category else None

    def validate(self, attrs):
        title = attrs.get('title', '')
        content = attrs.get('content', '')
        attrs['has_offensive_content'] = contains_offensive_content(f'{title} {content}')
        return attrs

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class NoteCreateSerializer(NoteSerializer):
    class Meta(NoteSerializer.Meta):
        fields = ['title', 'content', 'note_type', 'category', 'is_pinned']


class NoteUpdateSerializer(NoteSerializer):
    class Meta(NoteSerializer.Meta):
        fields = ['title', 'content', 'note_type', 'category', 'is_pinned']


class NoteListSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()
    category_color = serializers.SerializerMethodField()
    preview = serializers.SerializerMethodField()

    class Meta:
        model = Note
        fields = [
            'id', 'title', 'preview', 'note_type',
            'category', 'category_name', 'category_color',
            'is_pinned', 'has_offensive_content',
            'created_at', 'updated_at',
        ]

    def get_category_name(self, obj):
        return obj.category.name if obj.category else None

    def get_category_color(self, obj):
        return obj.category.color if obj.category else None

    def get_preview(self, obj):
        if not obj.content:
            return ''
        return obj.content[:150] + ('...' if len(obj.content) > 150 else '')
