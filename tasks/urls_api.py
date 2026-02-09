# tasks/urls_api.py
from django.urls import path
from . import api_views

urlpatterns = [
    # Задачи
    path('tasks/', api_views.TaskListAPI.as_view(), name='api-tasks-list'),
    path('tasks/<int:pk>/', api_views.TaskDetailAPI.as_view(), name='api-tasks-detail'),

    # Регистрация пользователя
    path('auth/register/', api_views.RegisterAPI.as_view(), name='api-register'),
    path('auth/login/', api_views.LoginAPI.as_view(), name='api-login'),
]
