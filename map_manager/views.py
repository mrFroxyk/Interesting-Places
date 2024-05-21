import random
from django.http import HttpResponse
from django.shortcuts import render
from .forms import MemoryForm
from .models import Memory


def index(request):
    """
    Тестовая страница
    """
    user = request.user
    if user.username not in ['528396568', '211604310']:
        return HttpResponse("Страница засекречена)))00)00)")

    if request.method == 'POST':
        print(request.POST)
        form = MemoryForm(request.POST, request.FILES)
        if form.is_valid():
            memory = form.save(commit=False)
            memory.author = request.user
            memory.save()
        else:
            print("ERROR, can't save memories", request.POST)

    rand_num = random.randint(1, 1000)
    form = MemoryForm()
    memory_list = Memory.objects.filter(author=user)[::-1]
    print(memory_list)
    context = {
        'memory_list': memory_list,
        'rand_num': rand_num,
        'form': form
    }

    return render(request, 'map_manager/test.html', context)
