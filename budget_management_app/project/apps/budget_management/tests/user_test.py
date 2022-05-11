from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from django.contrib.auth import get_user_model



class PublicUnitTest(TestCase):
    """Testcase used without authentication"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().create(
            'ashik'
            'ashi@gmailz.com',
            '8086477551',
            '1234',
        )

    def test_login_acess(self):
        """ tests for login access working or not """
        login_url = reverse("login")
        data = {
            'username': '8086477551',
            'password': '1234',
        }
        response = self.client.post(login_url, data=data)
        # print('#############', response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
