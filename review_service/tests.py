import json

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from review_service.models import Person, ReviewCycle


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

    def test_sign_out_with_success_case(self):
        self.test_sign_in_with_success_case()

        response = self.__client_request(self.client.post,
                                         reverse('review_service:account_sign_out'))

        self.assertEqual(response.status_code, 200)

    def test_sign_out_with_get_method(self):
        response = self.__client_request(self.client.get,
                                         reverse('review_service:account_sign_out'))

        self.assertEqual(response.status_code, 400)

    def test_create_policy_with_success_case(self):
        self.test_sign_in_with_success_case()

        self.__create_user('test2@test.com', 'test2', '123456')
        self.__create_user('test3@test.com', 'test3', '123456')

        response = self.__client_request(self.client.post,
                                         reverse('review_service:policy'),
                                         {'name': '2020 2Q 정기 리뷰',
                                          'reviewees': [2, 3],
                                          'question':
                                              {
                                                  'title': '이번 분기에서 나에게 가장 중요한 성과는 무엇이었나요?',
                                                  'description': '3개월 동안 수많은 문제들을 해결하시느라 고생 많으셨습니다! 그중에서도 가장 서비스에 임팩트가 컸다고 생각하는 일이 무엇이었는지 상세하게 적어주세요.'
                                              },
                                          })
        self.assertEqual(response.status_code, 200)
        review = ReviewCycle.objects.get(name__contains='2020')
        self.assertEqual(review.question.title, '이번 분기에서 나에게 가장 중요한 성과는 무엇이었나요?')
        self.assertEqual(review.reviewees.all()[0].email, 'test2@test.com')

    def test_create_policy_without_auth(self):
        self.__create_user('test2@test.com', 'test2', '123456')
        self.__create_user('test3@test.com', 'test3', '123456')

        response = self.__client_request(self.client.post,
                                         reverse('review_service:policy'),
                                         {'name': '2020 2Q 정기 리뷰',
                                          'reviewees': [1, 2],
                                          'question':
                                              {
                                                  'title': '이번 분기에서 나에게 가장 중요한 성과는 무엇이었나요?',
                                                  'description': '3개월 동안 수많은 문제들을 해결하시느라 고생 많으셨습니다! 그중에서도 가장 서비스에 임팩트가 컸다고 생각하는 일이 무엇이었는지 상세하게 적어주세요.'
                                              },
                                          })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(ReviewCycle.objects.count(), 0)

    def test_create_policy_without_required_field(self):
        self.test_sign_in_with_success_case()

        self.__create_user('test2@test.com', 'test2', '123456')
        self.__create_user('test3@test.com', 'test3', '123456')

        response = self.__client_request(self.client.post,
                                         reverse('review_service:policy'),
                                         {'reviewees': [1, 2],
                                          'question':
                                              {
                                                  'title': '이번 분기에서 나에게 가장 중요한 성과는 무엇이었나요?',
                                                  'description': '3개월 동안 수많은 문제들을 해결하시느라 고생 많으셨습니다! 그중에서도 가장 서비스에 임팩트가 컸다고 생각하는 일이 무엇이었는지 상세하게 적어주세요.'
                                              },
                                          })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(ReviewCycle.objects.count(), 0)
