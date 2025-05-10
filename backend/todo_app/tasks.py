import asyncio
from celery import shared_task
from django.utils import timezone
from .models import Task, UserProfile
import logging
from tgBot.notifications import send_telegram_notification

logger = logging.getLogger(__name__)

@shared_task
def check_due_tasks():
    loop = asyncio.get_event_loop()
    now = timezone.now()
    due_tasks = Task.objects.filter(due_date__lte=now, completed=False, notified=False)
    for task in due_tasks:
        try:
            user_profile = UserProfile.objects.get(user=task.user)
            telegram_id = user_profile.telegram_id
            message = f"Дедлайн задачи <b>{task.title}</b> наступил! Пора выполнить задачу!"
            success = loop.run_until_complete(send_telegram_notification(telegram_id, message))
            if success:
                task.notified = True
                task.save()
                logger.info(f"Notification sent for task '{task.title}' to user {task.user.username}")
            else:
                logger.warning(f"Failed to send notification for task '{task.title}' to user {task.user.username}")
        except UserProfile.DoesNotExist:
            logger.warning(f"No Telegram ID found for user {task.user.username}")
        except Exception as e:
            logger.error(f"Error processing task '{task.title}': {str(e)}")