import json
from django.test import TestCase
from django.urls import reverse
from auth_vk.models import VkUser


class ViewsTests(TestCase):
    """
    Тесты всех представлений /map_manager/view.py
    """

    def auth_and_get_user(self, username='1'):
        """
        Авторизирует пользователя для дальнейшего прохождения теста
        :param username: vk_id пользователя, который задается как pk для пользователя
        :return: объект модели VkUser
        """
        user = VkUser.objects.filter(pk=username).first()
        if not user:
            user = VkUser.objects.create(username=username, vk_id=username)
        self.client.force_login(user)
        return user

    def create_new_memory_and_get_response(self, title='title', content='content', coord1=55, coord2=35):
        """
        Создает новое воспоминание (перед этим надо авторизовать юзера или ничего не выйдет)
        :param title: заголовок воспоминания
        :param content: контент воспоминания
        :param coord1: первая координата на карте
        :param coord2: вторая координата на карте
        :return: response (главная страницу, на которой воспоминание отрендерится)
        """
        data = {
            'title': title,
            'content': content,
            'coord1': coord1,
            'coord2': coord2,
        }
        response = self.client.post(reverse('map_manager:create_memories'), data, follow=True)
        return response

    def update_memory_and_get_response(self, pk, title='title', content='content', coord1=55, coord2=35):
        """
        Обновляет воспоминание по pk
        :param pk: id воспоминания в бд
        :param title: заголовок воспоминания
        :param content: контент воспоминания
        :param coord1: первая координата на карте
        :param coord2: вторая координата на карте
        :return: response (главная страницу, на которой воспоминание отрендерится)
        """
        data = {
            'title': title,
            'content': content,
            'coord1': coord1,
            'coord2': coord2,
        }
        response = self.client.post(
            reverse('map_manager:update_memories', kwargs={'pk': pk}),
            data,
            follow=True
        )
        return response

    def test_new_user_see_auth_button(self):
        """
        Не авторизованные юзеры должны видеть страницу, где вместо кнопки
        'Добавить воспоминание', будет кнопку с предложением авторизоваться
        """
        response = self.client.get(reverse('map_manager:test'))
        self.assertContains(response, 'Хочется добавить новое воспоминание? Тогда жмякай по кнопке снизу')

    def test_new_user_havent_any_memories(self):
        """
        Проверка на то, при переходе нового юзера на страницу у него нету воспоминаний
        """
        self.auth_and_get_user()
        response = self.client.get(reverse('map_manager:test'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Добавить воспоминание')
        self.assertContains(response, 'У вас нет ни одного воспоминания')

    def test_create_memory(self):
        """
        Проверка, что авторизованный юзер при добавлении воспоминания видит его на главной странице
        """
        self.auth_and_get_user()
        response = self.create_new_memory_and_get_response(title='first memory')
        self.assertContains(response, 'first memory')

    def test_many_create_memories(self):
        """
        Проверка, что добавив несколько воспоминаний юзер будет их видеть на
        главной странице
        """
        self.auth_and_get_user()
        self.create_new_memory_and_get_response(title='first memory')
        self.create_new_memory_and_get_response(title='second memory')
        self.create_new_memory_and_get_response(title='third memory')
        response = self.client.get(reverse("map_manager:test"))
        self.assertContains(response, 'first memory')
        self.assertContains(response, 'second memory')
        self.assertContains(response, 'third memory')

    def test_dont_see_memories_after_logout(self):
        """
        Проверка, что после выхода из аккаунта не видно воспоминаний
        """
        self.auth_and_get_user()
        self.create_new_memory_and_get_response(title='first memory')
        self.create_new_memory_and_get_response(title='second memory')
        self.client.logout()
        response = self.client.get(reverse('map_manager:test'))
        self.assertContains(response, 'Хочется добавить новое воспоминание? Тогда жмякай по кнопке снизу')

    def test_attempt_to_create_memory_with_incorrect_data(self):
        """
        Нельзя передать некорректные данные и с ними отредачить воспоминание (существующее)
        """
        self.auth_and_get_user()
        data = {
            'title': "test memory",
            'content': "content",
        }
        response = self.client.post(reverse('map_manager:create_memories'), data, follow=True)
        self.assertNotContains(response, 'test memory')
        self.assertContains(response, 'Добавить воспоминание')
        self.assertContains(response, 'У вас нет ни одного воспоминания')

    def test_attempt_to_create_memory_without_auth(self):
        """
        Неавторизованный юзер не может добавить воспоминание
        """
        data = {
            'title': "test memory",
            'content': "content",
        }
        response = self.client.post(reverse('map_manager:create_memories'), data, follow=True)
        self.assertNotContains(response, 'test memory')
        self.assertContains(response, 'Хочется добавить новое воспоминание? Тогда жмякай по кнопке снизу')

    def test_update_memory(self):
        """
        Проверка на корректное обновление своего воспоминания юзером
        """
        self.auth_and_get_user()
        self.create_new_memory_and_get_response(title='first')
        self.create_new_memory_and_get_response(title='second')
        response = self.update_memory_and_get_response(2, title='2_but_edited')

        self.assertContains(response, 'first')
        self.assertNotContains(response, 'second')
        self.assertContains(response, '2_but_edited')

    def test_cant_update_memory_without_auth(self):
        """
        Неавторизованный юзер не может редачить какие-либо воспоминания:
        """
        self.auth_and_get_user()
        self.create_new_memory_and_get_response(title='first')
        self.client.logout()

        response = self.update_memory_and_get_response(pk=1, title='edited')
        self.assertNotContains(response, 'edited')
        self.assertContains(response, 'Хочется добавить новое воспоминание? Тогда жмякай по кнопке снизу')

    def test_cant_update_non_existent_memory(self):
        """
        Проверка на то, что нельзя отредачить несуществующую запись
        """
        self.auth_and_get_user()
        response = self.update_memory_and_get_response(2, title='2_but_edited')

        self.assertContains(response, 'Добавить воспоминание')
        self.assertContains(response, 'У вас нет ни одного воспоминания')
        self.assertNotContains(response, '2_but_edited')

    def test_user_cant_update_alien_memory(self):
        """
        Проверка, что юзер не может редактировать чужие воспоминания, зная их id
        """
        self.auth_and_get_user(username='1')
        self.create_new_memory_and_get_response(title='first')
        self.create_new_memory_and_get_response(title='second')

        self.client.logout()
        self.auth_and_get_user(username='2')
        self.update_memory_and_get_response(2, 'edit_alien_memory_hehehe')

        self.client.logout()
        self.auth_and_get_user(username='1')

        response = self.client.get(reverse('map_manager:test'))
        self.assertContains(response, 'first')
        self.assertContains(response, 'second')
        self.assertNotContains(response, 'edit_alien_memory_hehehe')

    def test_load_place_mark_from_server(self):
        """
        Тестирует функцию map_manager:get_place_data, которая должна вернуть серилизованный
        массив из объектов точек
        """
        self.auth_and_get_user(username='1')
        self.create_new_memory_and_get_response(title='first')
        self.create_new_memory_and_get_response(title='second')

        response = self.client.get(reverse('map_manager:get_place_data'))
        data = json.loads(response.content)

        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['title'], 'first')
        self.assertEqual(data[1]['title'], 'second')
