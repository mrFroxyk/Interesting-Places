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
    user = request.user
    if user.is_authenticated and user.is_staff:
        return render(request, 'map_manager/test.html', context)
    return render(request, 'map_manager/test.html', context)
    # return HttpResponse("Страница засекречена)))00)00)")
