from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import VkUserCreationForm, VkUserChangeForm
from .models import VkUser


class CustomUserAdmin(UserAdmin):
    """
    Модель для админки над юзером
    """
    add_form = VkUserCreationForm
    form = VkUserChangeForm
    model = VkUser
    list_display = ['username', 'email', 'is_staff', 'is_active', 'vk_id', 'vk_name', 'vk_photo_url']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('vk_id', 'vk_name', 'vk_photo_url')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('vk_id', 'vk_name', 'vk_photo_url')}),
    )


admin.site.register(VkUser, CustomUserAdmin)
