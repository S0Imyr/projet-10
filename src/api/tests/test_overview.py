from django.urls.base import reverse

from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from authentication.models import User


class APITests(APITestCase):
    client = APIClient()

    @classmethod
    def setUpClass(cls):
        cls.admin = User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')

    @classmethod
    def tearDownClass(cls):
        cls.admin = None
        User.objects.all().delete()

    def login_token(self, user):
        self.client.force_login(user=user)
        tokens = RefreshToken.for_user(user)
        access_token = str(tokens.access_token)
        return access_token

    def test_overview(self):
        access_token = self.login_token(self.admin)
        uri = reverse('api-overview')
        response = self.client.get(uri, HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)

    def test_overview_unauthorized(self):
        uri = reverse('api-overview')
        response = self.client.get(uri)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, response.content)
