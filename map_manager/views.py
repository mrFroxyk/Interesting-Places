from django.shortcuts import render


def index(request):
    """
    Тестовая страница
    """
    return render(request, 'map_manager/test.html')
