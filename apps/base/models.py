import uuid
from django.db import models
from django.contrib.auth.models import User


class BaseModels(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.CharField(max_length=32, default='system', verbose_name='创建者')
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True
