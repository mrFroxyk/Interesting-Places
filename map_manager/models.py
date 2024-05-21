from django.db import models
from auth_vk.models import VkUser


class Memory(models.Model):
    """
    Модель для воспоминания юзера
    """
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='images/')
    coord1 = models.DecimalField(max_digits=60, decimal_places=30)
    coord2 = models.DecimalField(max_digits=60, decimal_places=30)
    author = models.ForeignKey(VkUser, on_delete=models.CASCADE)  # Связываем с моделью пользователя Django
