from django.urls import path
from .views import login, auth

app_name = "auth_vk"
urlpatterns = [
    path('login/', login, name='login'),
    path('', auth, name='login'),
]
