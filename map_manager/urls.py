from django.urls import path
from .views import (
    main_map_page,
    get_place_data,
    update_view,
    create_memory
)

app_name = "map_manager"
urlpatterns = [
    path('test/', main_map_page, name='test'),
    path('update-memory/<int:pk>/', update_view, name='update_memories'),
    path('create-memory/', create_memory, name='create_memories'),
    path('get-place-marks-data-list/', get_place_data, name='get_place_data')
]
