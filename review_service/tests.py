from django.test import TestCase
from django.urls import reverse


class PolicyAPIViewTest(TestCase):
    def test_skeleton_sign_up(self):
        response = self.client.get(reverse('review_service:account_sign_up'))
        self.assertContains(response, "SIGN UP")

    def test_skeleton_policy_post(self):
        response = self.client.post(reverse("review_service:policy"))
        self.assertContains(response, "POST")

