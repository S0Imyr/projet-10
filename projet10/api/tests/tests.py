import pytest
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from authentication.models import User
from ..models import Contributor, Project

class APITests(APITestCase):
    client = APIClient()

    def setUp(self):
        self.user = User.objects.create_superuser('admin', 'admin@admin.com', 'admin123') 
        tokens = RefreshToken.for_user(self.user)
        self.token = str(tokens.access_token)

    def test_projects_unauthorized(self):
        response = self.client.get('/api/projects/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, response.content)

    def test_projects_list(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/api/projects/', HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)

    def test_projects_create(self):
        self.client.force_login(user=self.user)
        post_data = dict(title="Test title", description="Test description", type="back-end", author_user_id=self.user.id)
        response = self.client.post('/api/projects/', data=post_data, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.content)
    
    def test_list_contributors(self):
        self.client.force_login(user=self.user)
        project = Project.objects.create()
        Contributor.objects.create(project_id=project, user_id=self.user)
        response = self.client.get('/api/projects/1/users/', HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
