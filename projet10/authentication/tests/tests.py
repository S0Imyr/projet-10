import pytest
from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from authentication.models import User


class VehicleCreationTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser('admin', 'admin@admin.com', 'admin123') 
        tokens = RefreshToken.for_user(self.user)
        self.token = str(tokens.access_token)

    def test_overview(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/api/', HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 200)

    def test_overview_unauthorized(self):
        response = self.client.get('/api/')
        self.assertEqual(response.status_code, 401)

    def test_register(self):
        post_data = dict(username="username", email="email", first_name="first_name", last_name="last_name", password="password")
        response = self.client.post('/api/signup/', data=post_data)
        print(len(User.objects.all()))
        self.assertEqual(response.status_code, 201)

    def test_projects_unauthorized(self):
        response = self.client.get('/api/projects/')
        self.assertEqual(response.status_code, 401)

    def test_projects_list(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/api/projects/', HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 200)

    def test_projects_create(self):
        self.client.force_login(user=self.user)
        post_data = dict(title="Test title", description="Test description", type="Test type", author_user_id=1)
        response = self.client.post('/api/projects/', data=post_data, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 201)

