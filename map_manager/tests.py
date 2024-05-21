from django.test import TestCase
from django.urls import reverse


class SimpleTest(TestCase):
    """
    Самые первые тесты для интеграции с git actions
    """

    def test_spy_dont_see_main_page(self):
        """
        Проверка на то, что всякие шпионы не могут чекать сайт
        """
        response = self.client.get(reverse('map_manager:test'))
        self.assertEqual(response.status_code, 200)
        expected_text = "Страница засекречена"
        self.assertContains(response, expected_text)

    # def test_admin_can_see_main_page(self):
    #     """
    #     Проверка на то, что всякие шпионы не могут чекать сайт
    #     """
    #     self.client.login(username='528396568')
    #     response = self.client.get(reverse('map_manager:test'))
    #     self.assertEqual(response.status_code, 200)
    #     expected_text = "засекречена"
    #     self.assertContains(response, expected_text)
