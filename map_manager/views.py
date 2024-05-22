import random
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .forms import MemoryForm
from .models import Memory
from .serilizators import MemoriesSerializer


@api_view(['GET'])
def get_place_data(request):
    """
    Возвращает json из информации об объектах, в будущем можно добавить картинки
    """
    user = request.user
    memory_list = Memory.objects.filter(author=user)
    serializer = MemoriesSerializer(memory_list, many=True)
    return Response(serializer.data)


def update_view(request, pk):
    """
    Update метод для воспоминания
    :param pk: pk воспоминания
    """
    instance = Memory.objects.get(pk=pk)
    print(request.POST)
    if request.method == 'POST':
        form = MemoryForm(request.POST, instance=instance)
        # if form.is_valid():
        print(form.errors)
        form.save()
        print('Успешное обновление данных')
    return redirect(reverse('map_manager:test'))


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
    memory_list = Memory.objects.filter(author=user).order_by('-created_at')
    context = {
        'memory_list': memory_list,
        'rand_num': rand_num,
        'form': form
    }

    return render(request, 'map_manager/test.html', context)
