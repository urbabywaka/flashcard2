from django.urls import path
from . import views

app_name = 'flashcards'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('list/', views.flashcard_list, name='flashcard_list'),
    path('create/', views.flashcard_create, name='flashcard_create'),
    path('<int:pk>/', views.flashcard_detail, name='flashcard_detail'),
    path('<int:pk>/edit/', views.flashcard_edit, name='flashcard_edit'),
    path('<int:pk>/delete/', views.flashcard_delete, name='flashcard_delete'),
    path('study/', views.study_mode, name='study_mode'),
    path('<int:pk>/mark/', views.mark_flashcard, name='mark_flashcard'),
    path('study/end/', views.end_study_session, name='end_study_session'),
    path('export/', views.export_flashcards, name='export_flashcards'),
    path('import/', views.import_flashcards, name='import_flashcards'),
    path('statistics/', views.statistics, name='statistics'),
]
