from django.urls import path
from .views import index

app_name = "map_manager"
urlpatterns = [
    path('test/', index, name='test'),
    # path('test2/', index, name='test'),
]
