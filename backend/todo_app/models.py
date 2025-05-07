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
            # Генерируем уникальный ключ на основе времени и пользователя
            timestamp = timezone.now().isoformat()
            user_id = str(self.user.id if hasattr(self, 'user') else 0)
            data = f"{user_id}:{timestamp}".encode('utf-8')
            self.id = hashlib.sha256(data).hexdigest()[:64]
        super().save(*args, **kwargs)

class Category(CustomPKModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Task(CustomPKModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    categories = models.ManyToManyField(Category, related_name='tasks')

    def __str__(self):
        return self.title