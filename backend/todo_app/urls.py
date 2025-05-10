from django.urls import path
from .views import TaskListView, TaskDetailView, LinkTelegramIDView

urlpatterns = [
    path('tasks/', TaskListView.as_view(), name='task-list'),
    path('tasks/<str:id>/', TaskDetailView.as_view(), name='task-detail'),
    path('link_telegram_id/', LinkTelegramIDView.as_view(), name='link-telegram-id'),
]