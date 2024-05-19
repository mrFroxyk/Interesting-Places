import random

from django.shortcuts import render


def index(request):
    """
    Тестовая страница
    """
    rand_num = random.randint(1, 1000)
    context = {
        'rand_num': rand_num
    }

    return render(request, 'map_manager/test.html', context)
