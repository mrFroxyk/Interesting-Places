from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import VkUser


class VkUserCreationForm(UserCreationForm):
    """
    Модель для создания юзера
    """
    class Meta(UserCreationForm.Meta):
        model = VkUser
        fields = ('username', 'email', 'vk_id', 'vk_name', 'vk_photo_url')


class VkUserChangeForm(UserChangeForm):
    """
    Модель для редактирования юзера
    """
    class Meta:
        model = VkUser
        fields = ('username', 'email', 'vk_id', 'vk_name', 'vk_photo_url')
