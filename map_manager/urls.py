from django.urls import path
from .views import index, get_place_data

app_name = "map_manager"
urlpatterns = [
    path('test/', index, name='test'),
    path('get-place-marks-data-list/', get_place_data, name='get_place_data')
]
