from django.contrib import admin
from .models import FileUpload, QuizAnswer, QuizSession, Word


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ['word', 'lang', 'mastery', 'user', 'created_at']
    list_filter = ['lang', 'mastery']
    search_fields = ['word', 'meaning', 'user__username']


@admin.register(FileUpload)
class FileUploadAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'uploaded_at', 'expires_at']
    list_filter = ['uploaded_at']
    search_fields = ['title', 'user__username']


@admin.register(QuizSession)
class QuizSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'quiz_type', 'score_percent', 'total_questions', 'started_at']
    list_filter = ['quiz_type', 'lang']


@admin.register(QuizAnswer)
class QuizAnswerAdmin(admin.ModelAdmin):
    list_display = ['session', 'word', 'is_correct', 'user_answer']
    list_filter = ['is_correct']

