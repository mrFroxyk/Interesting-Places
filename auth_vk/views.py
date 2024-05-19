import json
import urllib.request
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings


def login(request):
    """
    Страница логина вк, пока что только тестовая
    """
    return render(request, 'auth_vk/login.html')


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
        print(data)
        return data


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
    print(user_id)
    return HttpResponse(str(get_user_data(access_token, fields)))
