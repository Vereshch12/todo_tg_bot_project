import hashlib
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class CustomPKModel(models.Model):
    id = models.CharField(max_length=64, primary_key=True, editable=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.id:
            # Генерируем уникальный ключ на основе времени и случайного значения
            timestamp = timezone.now().isoformat()
            # Добавляем случайное значение для уникальности (без использования random)
            random_seed = hashlib.sha256(str(timezone.now().microsecond).encode('utf-8')).hexdigest()[:8]
            # Используем user_id, если доступен, иначе 0
            user_id = str(self.user.id if hasattr(self, 'user') else 0)
            data = f"{user_id}:{timestamp}:{random_seed}".encode('utf-8')
            self.id = hashlib.sha256(data).hexdigest()[:64]
        super().save(*args, **kwargs)

class Category(CustomPKModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Автоматически устанавливается при создании
    updated_at = models.DateTimeField(auto_now=True)     # Обновляется при каждом сохранении

    def __str__(self):
        return self.name

class Task(CustomPKModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Автоматически устанавливается при создании
    updated_at = models.DateTimeField(auto_now=True)     # Обновляется при каждом сохранении
    due_date = models.DateTimeField()                    # Для уведомлений через Celery
    categories = models.ManyToManyField(Category, related_name='tasks')
    completed = models.BooleanField(default=False)       # Статус выполнения задачи
    notified = models.BooleanField(default=False)        # Флаг для отправки лишь одного уведомления после просрока

    def __str__(self):
        return self.title