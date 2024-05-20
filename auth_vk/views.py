import json
import urllib.request
from django.shortcuts import render, redirect, reverse
from django.conf import settings
from django.contrib.auth import login, logout
from .models import VkUser


def home_page_with_login(request):
    """
    Страница логина вк, пока что только тестовая
    """
    return render(request, 'auth_vk/profile.html')


def logout_user(request):
    """
    Страничка, на которую пользователя редиректит и выкидывает из
    аккаунта, после чего его редиректит на главную страницу.
    По факту юзер вообще не видит ее
    """
    logout(request)
    return redirect(reverse('auth_vk:login'))


def response_user_access_token(uuid, token):
    """
    Делает апи запрос к серверам VK, для обмена silent токена на access
    :param uuid: случайный идентификатор юзера, возвращается
    при первичной авторизации через вк
    :param token: silent токен, получаемый при авторизации через вк
    :return: access_token, user_id, fields пользователя
    """
    url = "https://api.vk.com/method/auth.exchangeSilentAuthToken"
    params = {
        'v': "5.131",
        'token': token,
        'access_token': settings.SERVICE_TOKEN,
        'uuid': uuid,
    }
    query_string = urllib.parse.urlencode(params)
    url_with_params = f"{url}?{query_string}"

    with urllib.request.urlopen(url_with_params) as response:
        response_data = response.read().decode()
        data = json.loads(response_data)['response']
        print(data)

        access_token = data['access_token']
        user_id = data['user_id']
        fields = 'photo_200'

        return access_token, user_id, fields


def get_user_data(access_token, fields):
    """
    По токенам пользователя получает его персональные данные
    :param access_token: access_token полученный из silent токена
    :param fields: поля, которые нужно запросить https://dev.vk.com/ru/reference/objects/user
    :return: Имя и ссылку на картинку аватарки
    """
    url = "https://api.vk.com/method/users.get"
    params = {
        'v': "5.199",
        'access_token': access_token,
        'fields': fields,
    }
    query_string = urllib.parse.urlencode(params)
    url_with_params = f"{url}?{query_string}"

    with urllib.request.urlopen(url_with_params) as response:
        response_data = response.read().decode()
        data = json.loads(response_data)['response'][0]
        photo_url = data['photo_200']
        full_name = data['first_name'] + ' ' + data['last_name']
        return full_name, photo_url


def auth(request):
    """
    Сюда вк редиректит юзера и гарантируется, что вернется uuid и token,
    которые используются для авторизации изера
    """
    print(request)
    payload = json.loads(request.GET.get('payload'))
    uuid = payload['uuid']
    token = payload['token']

    access_token, user_id, fields = response_user_access_token(uuid, token)
    full_name, photo_url = get_user_data(access_token, fields)

    try:
        user = VkUser.objects.get(vk_id=user_id)
    except VkUser.DoesNotExist:
        user = VkUser.objects.create(username=user_id, vk_name=full_name, vk_photo_url=photo_url, vk_id=user_id)

    login(request, user)
    return redirect(reverse("map_manager:test"))
