from django.test import TestCase
from django.urls import reverse


class SimpleTest(TestCase):
    """
    Самые первые тесты для интеграции с git actions
    """

    def test_test_page(self):
        """
        проверка на доступ к серверу и корректную работу сервера
        """
        response = self.client.get(reverse('map_manager:test'))
        self.assertEqual(response.status_code, 200)
        expected_text = "Место для прекрасного воспоминания"
        self.assertContains(response, expected_text)
