from django.contrib.auth.models import AbstractUser
from django.db import models


class VkUser(AbstractUser):
    """
    Модель пользователя через авторизацию вк
    """
    vk_id = models.CharField(max_length=100, unique=True)
    vk_name = models.CharField(max_length=255)
    vk_photo_url = models.URLField(max_length=500)

    def __str__(self):
        return self.username
