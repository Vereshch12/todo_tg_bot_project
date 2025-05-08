from celery import shared_task
from django.utils import timezone
from .models import Task
import logging

logger = logging.getLogger(__name__)

@shared_task
def check_due_tasks():
    now = timezone.now()
    due_tasks = Task.objects.filter(due_date__lte=now, completed=False, notified=False)
    for task in due_tasks:
        # пока просто выведем сообщение в лог, потом донастрою отправку в тг
        logger.warning(f"Task '{task.title}' is due for user {task.user.username}!")
        task.notified = True  # Отмечаем, что уведомление отправлено
        task.save()