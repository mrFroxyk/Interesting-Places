import random
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

    if request.method == 'POST':
        user = request.user
        instance = Memory.objects.filter(pk=pk).first()
        if instance and instance.author == user:
            form = MemoryForm(request.POST, instance=instance)
            if form.is_valid():
                form.save()
    return redirect(reverse('map_manager:test'))


def create_memory(request):
    """
    Метод для создания воспоминания
    """

    if request.method == 'POST':
        form = MemoryForm(request.POST, request.FILES)
        if form.is_valid():
            memory = form.save(commit=False)
            memory.author = request.user
            memory.save()
    return redirect(reverse('map_manager:test'))


def main_map_page(request):
    """
    Ключевая страница с воспоминаниями. Здесь юзеру выводятся все его воспоминания
    (или пишется, что их нет) и есть форма для создания новых
    """
    user = request.user
    if user.is_authenticated:
        memory_list = Memory.objects.filter(author=user).order_by('-created_at')
    else:
        memory_list = None
    rand_num = random.randint(1, 1000)

    context = {
        'memory_list': memory_list,
        'rand_num': rand_num,
    }

    return render(request, 'map_manager/main_map_page.html', context)
