from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from authentication.models import User


class AuthTests(APITestCase):
    client = APIClient()

    @classmethod
    def setUpClass(cls):
        """Log Admin"""
        cls.user = User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
        tokens = RefreshToken.for_user(cls.user)
        cls.token = str(tokens.access_token)

    @classmethod
    def tearDownClass(cls):
        cls.user = None
        cls.token = None
        User.objects.all().delete()

    def test_overview(self):
        self.client.force_login(user=self.user)
        uri = reverse('api-overview')
        response = self.client.get(uri, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)

    def test_overview_unauthorized(self):
        uri = reverse('api-overview')
        response = self.client.get(uri)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, response.content)

    def test_register(self):
        uri = reverse('register')
        post_data = dict(
            username="username", email="email@test.com",
            first_name="first_name", last_name="last_name", password="password")
        response = self.client.post(uri, data=post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.content)
