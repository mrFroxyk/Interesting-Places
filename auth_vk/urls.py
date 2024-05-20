from django.urls import path
from .views import home_page_with_login, auth, logout_user

app_name = "auth_vk"
urlpatterns = [
    path('profile/', home_page_with_login, name='login'),
    path('logout/', logout_user, name='logout'),
    path('', auth, name='auth'),
]
