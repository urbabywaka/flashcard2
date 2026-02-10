from django.contrib import admin
from .models import Flashcard, StudySession


@admin.register(Flashcard)
class FlashcardAdmin(admin.ModelAdmin):
    list_display = ['front', 'topic', 'user', 'created_at', 'times_reviewed', 'is_known']
    list_filter = ['topic', 'is_known', 'created_at']
    search_fields = ['front', 'back', 'topic', 'user__username']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Content', {
            'fields': ('user', 'front', 'back', 'topic')
        }),
        ('Study Progress', {
            'fields': ('times_reviewed', 'times_correct', 'last_reviewed', 'is_known')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(StudySession)
class StudySessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'started_at', 'ended_at', 'cards_studied', 'cards_known', 'topic']
    list_filter = ['started_at', 'topic']
    search_fields = ['user__username', 'topic']
    date_hierarchy = 'started_at'
    readonly_fields = ['started_at']
