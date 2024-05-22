from rest_framework.serializers import ModelSerializer
from .models import Memory


class MemoriesSerializer(ModelSerializer):
    """
    Серилизатор для представления воспоминаний
    """
    class Meta:
        model = Memory
        fields = '__all__'
