import json

from django.test import TestCase
from django.urls import reverse

from review_service.models import Person, ReviewCycle, Question


class ReviewServiceTest(TestCase):
    @classmethod
    def __create_person(cls, email, name, password):
        return Person.objects.create_user(email, name, password)

    @classmethod
    def setUpTestData(cls):
        cls.person1 = cls.__create_person('test@test.com', 'test', '123456')
        cls.person2 = cls.__create_person('test2@test.com', 'test2', '123456')
        cls.person3 = cls.__create_person('test3@test.com', 'test3', '123456')

        # Default ReviewCycle count is set to 1 if uncomment these lines, which might be an improper situation.
        # q = Question.objects.create(title="Review Question", description="Policy for Test")
        # rc = ReviewCycle.objects.create(creator=p, name="Review Policy", question=q)
        # rc.reviewees.set([2, 3])

    @staticmethod
    def __client_request(method, path, data=None):
        if method.__name__ is 'get':
            return method(path, data)
        if data is None:
            return method(path, content_type='application/json')
        else:
            return method(path, json.dumps(data), content_type='application/json')

    @staticmethod
    def __parse_response(response):
        return json.loads(response.content.decode("utf-8"))

    def __setUpTestReviewCycle(self):
        p = Person.objects.get(pk=1)
        rc = ReviewCycle.objects.create(creator=p, name="Review Policy")
        Question.objects.create(review_cycle=rc, title="Review Question", description="Policy for Test")
        rc.reviewees.set([2, 3])

    def __setUpLoginState(self, person=None):
        if person:
            self.client.force_login(person)
        else:
            self.client.force_login(self.person1)

    def test_sign_up_with_get_method(self):
        response = self.__client_request(self.client.get,
                                         reverse('review_service:account_sign_up'))
        self.assertEqual(response.status_code, 400)

    def test_sign_up_with_success_case(self):
        response = self.__client_request(self.client.post,
                                         reverse('review_service:account_sign_up'),
                                         {'email': 'test_new@test.com',
                                          'name': 'test_new',
                                          'password': '123456'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Person.objects.get(email='test_new@test.com').name, 'test_new')

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
        # self.test_sign_up_with_success_case()

        response = self.__client_request(self.client.post,
                                         reverse('review_service:account_sign_in'),
                                         {'email': 'test@test.com',
                                          'password': '123456'})

        self.assertEqual(response.status_code, 200)

    def test_sign_in_with_wrong_password_case(self):
        response = self.__client_request(self.client.post,
                                         reverse('review_service:account_sign_in'),
                                         {'email': 'test@test.com',
                                          'password': '123'})

        # self.assertEqual(response.status_code, 400)
        self.assertContains(response, 'Incorrect', status_code=400)

    def test_sign_in_with_no_id_case(self):
        response = self.__client_request(self.client.post,
                                         reverse('review_service:account_sign_in'),
                                         {'email': 'no@test.com',
                                          'password': '123456'})

        self.assertContains(response, 'Incorrect', status_code=400)

    def test_sign_in_with_no_id_wrong_password_case(self):
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
        self.assertEqual(response.status_code, 201)
        review = ReviewCycle.objects.get(name__contains='2020')
        self.assertEqual(review.question.title, '이번 분기에서 나에게 가장 중요한 성과는 무엇이었나요?')
        self.assertEqual(review.reviewees.all()[0].email, 'test2@test.com')

    def test_create_policy_without_auth(self):
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

        self.assertEqual(response.status_code, 400)
        self.assertEqual(ReviewCycle.objects.count(), 0)

    def test_create_policy_without_required_field(self):
        self.test_sign_in_with_success_case()

        response = self.__client_request(self.client.post,
                                         reverse('review_service:policy'),
                                         {'reviewees': [2, 3],
                                          'question':
                                              {
                                                  'title': '이번 분기에서 나에게 가장 중요한 성과는 무엇이었나요?',
                                                  'description': '3개월 동안 수많은 문제들을 해결하시느라 고생 많으셨습니다! 그중에서도 가장 서비스에 임팩트가 컸다고 생각하는 일이 무엇이었는지 상세하게 적어주세요.'
                                              },
                                          })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(ReviewCycle.objects.count(), 0)

    def test_read_policy_with_success_case(self):
        self.__setUpLoginState()
        self.__setUpTestReviewCycle()

        response = self.__client_request(self.client.get,
                                         reverse('review_service:policy_one_argument', args=(1,)))

        data = self.__parse_response(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['name'], 'Review Policy')
        self.assertEqual(data['creator'], 1)
        self.assertEqual(data['reviewees'], [2, 3])
        self.assertEqual(data['question']['title'], 'Review Question')
        self.assertEqual(data['question']['description'], 'Policy for Test')

    def test_read_policy_with_not_existing_one(self):
        self.__setUpLoginState()

        response = self.__client_request(self.client.get,
                                         reverse('review_service:policy_one_argument', args=(1,)))

        self.assertEqual(response.status_code, 400)

    def test_read_policy_without_argument(self):
        self.__setUpLoginState()
        self.__setUpTestReviewCycle()

        response = self.__client_request(self.client.get,
                                         reverse('review_service:policy'))

        self.assertEqual(response.status_code, 404)

    def test_read_policy_without_permission(self):
        self.__setUpLoginState(self.person2)
        self.__setUpTestReviewCycle()

        response = self.__client_request(self.client.get,
                                         reverse('review_service:policy_one_argument', args=(1,)))

        self.assertEqual(response.status_code, 400)

    def test_update_policy_every_field_with_success_case(self):
        self.__setUpLoginState()
        self.__setUpTestReviewCycle()

        response = self.__client_request(self.client.put,
                                         reverse('review_service:policy_one_argument', args=(1,)),
                                         {'name': '2020 3Q 정기 리뷰',
                                          'reviewees': [3],
                                          'question':
                                              {
                                                  'title': '지난 분기에서 나에게 가장 중요한 성과는 무엇이었나요?',
                                                  'description': '1개월 동안 수많은 문제들을 해결하시느라 고생 많으셨습니다!'
                                              },
                                          })

        self.assertEqual(response.status_code, 200)
        review = ReviewCycle.objects.get(name__contains='3Q')
        self.assertEqual(review.question.title, '지난 분기에서 나에게 가장 중요한 성과는 무엇이었나요?')
        self.assertEqual(review.reviewees.all()[0].email, 'test3@test.com')

    def test_update_policy_without_every_field(self):
        self.__setUpLoginState()
        self.__setUpTestReviewCycle()

        response = self.__client_request(self.client.put,
                                         reverse('review_service:policy_one_argument', args=(1,)),
                                         {'name': '2020 3Q 정기 리뷰'})

        self.assertEqual(response.status_code, 400)

    def test_update_policy_with_not_existing_one(self):
        self.__setUpLoginState()

        response = self.__client_request(self.client.put,
                                         reverse('review_service:policy_one_argument', args=(1,)),
                                         {'name': '2020 3Q 정기 리뷰',
                                          'reviewees': [3],
                                          'question':
                                              {
                                                  'title': '지난 분기에서 나에게 가장 중요한 성과는 무엇이었나요?',
                                                  'description': '1개월 동안 수많은 문제들을 해결하시느라 고생 많으셨습니다!'
                                              },
                                          })

        self.assertEqual(response.status_code, 400)

    def test_update_policy_without_auth(self):
        self.__setUpTestReviewCycle()

        response = self.__client_request(self.client.put,
                                         reverse('review_service:policy_one_argument', args=(1,)),
                                         {'name': '2020 3Q 정기 리뷰',
                                          'reviewees': [3],
                                          'question':
                                              {
                                                  'title': '지난 분기에서 나에게 가장 중요한 성과는 무엇이었나요?',
                                                  'description': '1개월 동안 수많은 문제들을 해결하시느라 고생 많으셨습니다!'
                                              },
                                          })

        self.assertEqual(response.status_code, 400)

    def test_delete_policy_with_success_case(self):
        self.__setUpLoginState()
        self.__setUpTestReviewCycle()

        response = self.__client_request(self.client.delete,
                                         reverse('review_service:policy_one_argument', args=(1,)))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(ReviewCycle.objects.count(), 0)
        self.assertEqual(Question.objects.count(), 0)

    def test_delete_policy_with_not_existing_one(self):
        self.__setUpLoginState()

        response = self.__client_request(self.client.delete,
                                         reverse('review_service:policy_one_argument', args=(1,)))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(ReviewCycle.objects.count(), 0)
        self.assertEqual(Question.objects.count(), 0)

    def test_delete_policy_without_permission(self):
        self.__setUpLoginState(self.person2)
        self.__setUpTestReviewCycle()

        response = self.__client_request(self.client.delete,
                                         reverse('review_service:policy_one_argument', args=(1,)))

        self.assertEqual(response.status_code, 400)
