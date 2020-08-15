from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from review_service.models import Person


class PolicyAPIViewTest(TestCase):
    def test_sign_up_with_get_method(self):
        response = self.client.get(reverse('review_service:account_sign_up'))
        self.assertEqual(response.status_code, 400)

    def test_sign_up_with_success_case(self):
        response = self.client.post(reverse('review_service:account_sign_up'),
                                    {'email': 'test@test.com',
                                     'name': 'test',
                                     'password': '123456'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Person.objects.get(email='test@test.com').name, 'test')

    def test_sign_up_with_failure_case(self):
        response = self.client.post(reverse('review_service:account_sign_up'),
                                    {'email': 'test2@test.com',
                                     'password': '123456'})
        self.assertEqual(response.status_code, 400)
