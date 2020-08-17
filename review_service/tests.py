import json

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from review_service.models import Person


class ReviewServiceTest(TestCase):
    def __client_request(self, method, path, data=None):
        if data is None:
            return method(path, content_type='application/json')
        else:
            return method(path, json.dumps(data), content_type='application/json')

    def __create_user(self, email, name, password):
        return Person.objects.create_user(email, name, password)

    def test_sign_up_with_get_method(self):
        response = self.__client_request(self.client.get,
                                         reverse('review_service:account_sign_up'))
        self.assertEqual(response.status_code, 400)

    def test_sign_up_with_success_case(self):
        response = self.__client_request(self.client.post,
                                         reverse('review_service:account_sign_up'),
                                         {'email': 'test@test.com',
                                          'name': 'test',
                                          'password': '123456'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Person.objects.get(email='test@test.com').name, 'test')

    def test_sign_up_with_failure_case(self):
        response = self.__client_request(self.client.post,
                                         reverse('review_service:account_sign_up'),
                                         {'email': 'test2@test.com',
                                          'password': '123456'})
        self.assertEqual(response.status_code, 400)

    def test_sign_in_with_get_method(self):
        response = self.__client_request(self.client.get,
                                         reverse('review_service:account_sign_in'))
        self.assertEqual(response.status_code, 400)

    def test_sign_in_with_success_case(self):
        self.__create_user('test@test.com', 'test', '123456')
        # self.test_sign_up_with_success_case()

        response = self.__client_request(self.client.post,
                                         reverse('review_service:account_sign_in'),
                                         {'email': 'test@test.com',
                                          'password': '123456'})

        self.assertEqual(response.status_code, 200)

    def test_sign_in_with_wrong_password_case(self):
        self.__create_user('test@test.com', 'test', '123456')

        response = self.__client_request(self.client.post,
                                         reverse('review_service:account_sign_in'),
                                         {'email': 'test@test.com',
                                          'password': '123'})

        # self.assertEqual(response.status_code, 400)
        self.assertContains(response, 'Incorrect', status_code=400)

    def test_sign_in_with_no_id_case(self):
        self.__create_user('test@test.com', 'test', '123456')

        response = self.__client_request(self.client.post,
                                         reverse('review_service:account_sign_in'),
                                         {'email': 'no@test.com',
                                          'password': '123456'})

        self.assertContains(response, 'Incorrect', status_code=400)

    def test_sign_in_with_no_id_wrong_password_case(self):
        self.__create_user('test@test.com', 'test', '123456')

        response = self.__client_request(self.client.post,
                                         reverse('review_service:account_sign_in'),
                                         {'email': 'no@test.com',
                                          'password': '123'})

        self.assertContains(response, 'Incorrect', status_code=400)
