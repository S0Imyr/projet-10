from django.urls.base import reverse

from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from authentication.models import User

from api.models import Project, Contributor,\
    CONTRIBUTOR_PERMISSION_CHOICES, PROJECT_TYPE_CHOICES

"""
CONTRIBUTOR_PERMISSION_CHOICES = (('not allowed','not allowed'), ('allowed','allowed'))
"""

class APITests(APITestCase):
    client = APIClient()

    @classmethod
    def setUpClass(cls):
        cls.admin = User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
        cls.users = [
            User.objects.create_user(
                username="Username1", email="test1@test.com",
                password="password1", first_name="firstname1", last_name="lastname1"),
            User.objects.create_user(
                username="Username2", email="test2@test.com",
                password="password2", first_name="firstname2", last_name="lastname2"),
            User.objects.create_user(
                username="Username3", email="test3@test.com",
                password="password3", first_name="firstname3", last_name="lastname3"),
            User.objects.create_user(
                username="Username4", email="test4@test.com",
                password="password4", first_name="firstname4", last_name="lastname4"),
        ]
        cls.notcontributor = User.objects.create_user(
            username="Username5", email="test5@test.com",
            password="password5", first_name="firstname5", last_name="lastname5")
        cls.projects = [
            Project.objects.create(
                title="Project1", author_user_id=cls.users[0],
                description="description1", type=PROJECT_TYPE_CHOICES[0]),
            Project.objects.create(
                title="Project2", author_user_id=cls.users[1],
                description="description2", type=PROJECT_TYPE_CHOICES[1]),
            Project.objects.create(
                title="Project3", author_user_id=cls.users[2],
                description="description3", type=PROJECT_TYPE_CHOICES[2]),
            Project.objects.create(
                title="Project4", author_user_id=cls.users[3],
                description="description4", type=PROJECT_TYPE_CHOICES[3]),
        ]
        Contributor.objects.create(
            project_id=cls.projects[0], permission=CONTRIBUTOR_PERMISSION_CHOICES[1],
            role="contributor", user_id=cls.users[1])
        Contributor.objects.create(
            project_id=cls.projects[0], permission=CONTRIBUTOR_PERMISSION_CHOICES[1],
            role="contributor", user_id=cls.users[2])
        Contributor.objects.create(
            project_id=cls.projects[0], permission=CONTRIBUTOR_PERMISSION_CHOICES[1],
            role="contributor", user_id=cls.users[3])
        Contributor.objects.create(
            project_id=cls.projects[0], permission=CONTRIBUTOR_PERMISSION_CHOICES[1],
            role="contributor", user_id=cls.users[0])

    @classmethod
    def tearDownClass(cls):
        cls.admin = None
        User.objects.all().delete()

    def login_token(self, user):
        self.client.force_login(user=user)
        tokens = RefreshToken.for_user(user)
        access_token = str(tokens.access_token)
        return access_token

    def test_list_contributors_unauthenticated(self):
        access_token = ""
        project = self.projects[0]
        uri = reverse('project-users-list', args=[project.id])
        response = self.client.get(uri, HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, response.content)

    def test_list_contributors(self):
        access_token = self.login_token(user=self.users[0])
        project = self.projects[0]
        uri = reverse('project-users-list', args=[project.id])
        response = self.client.get(uri, HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)

    def test_list_contributors_not_contributor(self):
        access_token = self.login_token(user=self.notcontributor)
        project = self.projects[0]
        uri = reverse('project-users-list', args=[project.id])
        response = self.client.get(uri, HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.content)

    def test_create_contributor_unauthenticated(self):
        access_token = ""
        project = self.projects[0]
        post_data=dict(permission="allowed",role="contributor", user_id=self.notcontributor.id)
        uri = reverse('project-users-list', args=[project.id])
        response = self.client.post(uri, data=post_data, HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, response.content)

    def test_create_contributor(self):
        access_token = self.login_token(user=self.users[0])
        project = self.projects[0]
        post_data=dict(permission="allowed",role="contributor", user_id=self.notcontributor.id)
        uri = reverse('project-users-list', args=[project.id])
        response = self.client.post(uri, data=post_data, HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.content)
   
    def test_create_contributor_not_contributor(self):
        access_token = self.login_token(user=self.notcontributor)
        project = self.projects[0]
        post_data=dict(permission="allowed",role="contributor", user_id=self.notcontributor.id)
        uri = reverse('project-users-list', args=[project.id])
        response = self.client.post(uri, data=post_data, HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.content)

    def test_retrieve_contributor_unauthenticated(self):
        pass

    def test_retrieve_contributor(self):
        pass
    
    def test_retrieve_contributor_not_contributor(self):
        pass

    def test_update_contributor_unauthenticated(self):
        pass

    def test_update_contributor(self):
        pass
    
    def test_update_contributor_not_contributor(self):
        pass

    def test_delete_contributor_unauthenticated(self):
        pass

    def test_delete_contributor(self):
        pass
    
    def test_delete_contributor_not_contributor(self):
        pass