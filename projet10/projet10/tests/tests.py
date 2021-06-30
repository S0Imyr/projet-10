from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from authentication.models import User


class AuthTests(APITestCase):
    client = APIClient()

    @classmethod
    def setUpClass(cls):
        cls.admin = User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
        cls.user = User.objects.create(
            username="Username1", email="test1@test.com",
            password="password1", first_name="firstname1", last_name="lastname1")

                
    @classmethod
    def tearDownClass(cls):
        cls.admin = None
        User.objects.all().delete()
    
    def login_token(self, user):
        access_token = AccessToken.for_user(user)
        refresh_token = RefreshToken.for_user(user)
        return str(access_token), str(refresh_token)

    def test_login(self):
        uri = reverse('login')
        print('Username :', self.user.username)
        print('password :', self.user.password)
        print('Is active :', self.user.is_active)
        post_data = dict(username=self.user.username, password=self.user.password)
        response = self.client.post(uri, data=post_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)

    def test_refresh(self):
        refresh_token = self.login_token(self.user)[1]
        post_data = dict(refresh=refresh_token)
        uri = reverse('refresh')
        response = self.client.post(uri, data=post_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
