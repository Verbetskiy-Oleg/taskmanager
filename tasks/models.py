from django.db import models
from django.utils import timezone

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)  # вместо auto_now_add=True
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
