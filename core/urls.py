from django.urls import include, path
from . import views
from .views import ai_dictionary, ai_translate
from .views import ai_flashcard, ai_quiz

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),

    path('health/', views.health_check, name='health_check'),

    path('import/', views.import_excel, name='import_excel'),
    path('words/', views.word_list, name='word_list'),
    path('words/<int:word_id>/mastery/', views.update_mastery, name='update_mastery'),

    path('flashcard/', views.flashcard, name='flashcard'),

    path('quiz/', views.quiz_home, name='quiz_home'),
    path('quiz/start/', views.quiz_start, name='quiz_start'),
    path('quiz/<int:session_id>/<int:q_index>/', views.quiz_question, name='quiz_question'),
    path('quiz/<int:session_id>/done/', views.quiz_result, name='quiz_result'),
    path('quiz/history/', views.quiz_history, name='quiz_history'),

    path('upload/', views.upload_file, name='upload_file'),
    path('files/', views.file_list, name='file_list'),
    path('files/<int:pk>/', views.view_file, name='view_file'),
    path('files/<int:pk>/note/', views.save_note, name='save_note'),

    # AI
    path("ai-translate/", ai_translate, name="ai_translate"),
    path("ai-flashcard/", ai_flashcard),
    path("ai-quiz/", ai_quiz),
    path("ai-dictionary/", ai_dictionary),
    path("accounts/", include("allauth.urls")),
    
    path("privacy/", views.privacy_policy, name="privacy"),
    path("delete-data/", views.delete_data, name="delete_data"),
]