from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError

class Task(models.Model):
    STATUS_CHOICES = (
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    deadline = models.DateField(null=True, blank=True)  # можно оставить пустым
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def clean(self):
        """
        Проверка: описание минимум 10 символов и дедлайн не в прошлом
        """
        # Проверка описания
        if self.description and len(self.description) < 10:
            raise ValidationError("Описание должно быть минимум 10 символов")

        # Проверка дедлайна, только если он указан
        if self.deadline and self.deadline < timezone.now().date():
            raise ValidationError("Дедлайн не может быть в прошлом")
