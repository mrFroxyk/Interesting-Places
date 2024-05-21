from django import forms
from .models import Memory


class MemoryForm(forms.ModelForm):
    """
    Форма для создания воспоминания
    """

    class Meta:
        model = Memory
        fields = ['title', 'content', 'image', 'coord1', 'coord2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False
