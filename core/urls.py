from django.urls import path
from . import views

# BUG FIX: 3 paths upload_file/files/files/<pk> trước đây nằm NGOÀI urlpatterns []
# → chỉ là floating expressions, không được đăng ký → 404 mọi request

urlpatterns = [
    # ── Core ──────────────────────────────────────────────────────────────────
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),

    # ── Words ─────────────────────────────────────────────────────────────────
    path('import/', views.import_excel, name='import_excel'),
    path('words/', views.word_list, name='word_list'),
    path('words/<int:word_id>/mastery/', views.update_mastery, name='update_mastery'),

    # ── Flashcard ─────────────────────────────────────────────────────────────
    path('flashcard/', views.flashcard, name='flashcard'),

    # ── Quiz ──────────────────────────────────────────────────────────────────
    path('quiz/', views.quiz_home, name='quiz_home'),
    path('quiz/start/', views.quiz_start, name='quiz_start'),
    path('quiz/<int:session_id>/<int:q_index>/', views.quiz_question, name='quiz_question'),
    path('quiz/<int:session_id>/done/', views.quiz_result, name='quiz_result'),
    path('quiz/history/', views.quiz_history, name='quiz_history'),

    # ── File upload ───────────────────────────────────────────────────────────
    path('upload/', views.upload_file, name='upload_file'),
    path('files/', views.file_list, name='file_list'),
    path('files/<int:pk>/', views.view_file, name='view_file'),
    path('files/<int:pk>/note/', views.save_note, name='save_note'),
]