from django.urls import path
from .views import (
    task_list_page,
    task_detail_page,
    task_create_page,
    task_update_page,
    task_delete_page,
    login_page,
    register_page,
    logout_page,
)

urlpatterns = [
    path('pages/tasks/', task_list_page, name='task_list_page'),
    path('pages/tasks/<int:pk>/', task_detail_page, name='task_detail_page'),
    path('pages/tasks/create/', task_create_page, name='task_create_page'),
    path('pages/tasks/<int:pk>/edit/', task_update_page, name='task_update_page'),
    path('pages/tasks/<int:pk>/delete/', task_delete_page, name='task_delete_page'),

    path('pages/auth/register/', register_page, name='register_page'),
    path('pages/auth/login/', login_page, name='login_page'),
    path('pages/auth/logout/', logout_page, name='logout_page'),
]
