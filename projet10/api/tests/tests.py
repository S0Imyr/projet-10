import pytest, random
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from authentication.models import User

from ..models import Project, Contributor, Issue, Comment, \
                        CONTRIBUTOR_PERMISSION_CHOICES, PROJECT_TYPE_CHOICES, \
                        ISSUE_PRIORITY_CHOICES, ISSUE_TAG_CHOICES, ISSUE_STATUS_CHOICES

@pytest.fixture()
def new_user_factory(db):
    def create_app_user(
        username: str,
        email: str = "test@test.com",
        password: str = None,
        first_name: str = "firstname",
        last_name: str = "lastname",
        is_staff: str = False,
        is_superuser: str = False,
        is_active: str = True,
    ):
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_active=is_active,
        )
        return user
    return create_app_user


@pytest.fixture()
def new_project_factory(db):
    def create_new_project(
        title: str,
        author: User,
        description: str = "Some description",
        type: str = random.choice(PROJECT_TYPE_CHOICES),
    ):
        project = Project.objects.create(title=title, author_user_id=author, description=description, type = type)
        return project
    return create_new_project

@pytest.fixture()
def environnement(db, new_user_factory, new_project_factory):
    users = [new_user_factory("UserTest1", "test1@test.com", "password1", "Name1"),
             new_user_factory("UserTest2", "test2@test.com", "password2", "Name2"),
             new_user_factory("UserTest3", "test3@test.com", "password3", "Name3"),
             new_user_factory("UserTest4", "test4@test.com", "password4", "Name4")]
    projects = [new_project_factory("Projet1", users[1]),
                new_project_factory("Projet2", users[2]),
                new_project_factory("Projet3", users[3]),
                new_project_factory("Projet4", users[4])]
    return users, projects



class APITests(APITestCase):
    client = APIClient()
    

    def setUp(self):
        User.objects.all().delete()
        Project.objects.all().delete()
        Contributor.objects.all().delete()
        self.admin = User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
        self.users = [User.objects.create(username="Username1", email="test1@test.com", password="password1", first_name="firstname1", last_name="lastname1"),
                      User.objects.create(username="Username2", email="test2@test.com", password="password2", first_name="firstname2", last_name="lastname2"),
                      User.objects.create(username="Username3", email="test3@test.com", password="password3", first_name="firstname3", last_name="lastname3"),
                      User.objects.create(username="Username4", email="test4@test.com", password="password4", first_name="firstname4", last_name="lastname4"),
        ]
        self.notcontributor = User.objects.create(username="Username5", email="test5@test.com", password="password5", first_name="firstname5", last_name="lastname5")
        self.projects = [Project.objects.create(title="Project1", author_user_id=self.users[0], description="description1", type=random.choices(PROJECT_TYPE_CHOICES)),
                         Project.objects.create(title="Project2", author_user_id=self.users[1], description="description2", type=random.choices(PROJECT_TYPE_CHOICES)),
                         Project.objects.create(title="Project3", author_user_id=self.users[2], description="description3", type=random.choices(PROJECT_TYPE_CHOICES)),
                         Project.objects.create(title="Project4", author_user_id=self.users[3], description="description4", type=random.choices(PROJECT_TYPE_CHOICES)),
        ]
        Contributor.objects.create(project_id=self.projects[0], permission=random.choices(CONTRIBUTOR_PERMISSION_CHOICES), role="contributor", user_id=self.users[1])
        Contributor.objects.create(project_id=self.projects[0], permission=random.choices(CONTRIBUTOR_PERMISSION_CHOICES), role="contributor", user_id=self.users[2])
        Contributor.objects.create(project_id=self.projects[0], permission=random.choices(CONTRIBUTOR_PERMISSION_CHOICES), role="contributor", user_id=self.users[3])
        Contributor.objects.create(project_id=self.projects[0], permission=random.choices(CONTRIBUTOR_PERMISSION_CHOICES), role="contributor", user_id=self.users[0])


    def test_list_projects_unauthenticated(self):
        response = self.client.get('/api/projects/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, response.content)

    def test_list_projects(self):
        self.client.force_login(user=self.users[0])
        tokens = RefreshToken.for_user(self.users[0])
        access_token = str(tokens.access_token)
        response = self.client.get('/api/projects/', HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)

    def test_create_project_unauthenticated(self):
        access_token = ""
        post_data = dict(title="Test title", description="Test description", type="back-end", author_user_id=self.users[0])
        response = self.client.post('/api/projects/', data=post_data, HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, response.content)

    def test_create_project(self):
        self.client.force_login(user=self.users[0])
        tokens = RefreshToken.for_user(self.users[0])
        access_token = str(tokens.access_token)
        post_data = dict(title="Test title", description="Test description", type="back-end", author_user_id=self.users[0])
        response = self.client.post('/api/projects/', data=post_data, HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.content)

    def test_retrieve_project_unauthenticated(self):
        access_token = ""
        project = self.projects[0]
        response = self.client.get(f'/api/projects/{project.id}', HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, response.content)


    def test_retrieve_project(self):
        self.client.force_login(user=self.users[0])
        tokens = RefreshToken.for_user(self.users[0])
        access_token = str(tokens.access_token)
        project = self.projects[0]
        response = self.client.get(f'/api/projects/{project.id}', HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)


    def test_retrieve_project_not_contributor(self):
        self.client.force_login(user=self.notcontributor)
        tokens = RefreshToken.for_user(self.notcontributor)
        access_token = str(tokens.access_token)
        project = self.projects[0]
        response = self.client.get(f'/api/projects/{project.id}', HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.content)

    def test_update_project_unauthenticated(self):
        access_token = ""
        project = self.projects[0]
        post_data = dict(title="Update title", description="Update description", type="back-end")
        response = self.client.put(f'/api/projects/{project.id}', data=post_data, HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, response.content)

    def test_update_project(self):
        self.client.force_login(user=self.users[0])
        tokens = RefreshToken.for_user(self.users[0])
        access_token = str(tokens.access_token)
        project = self.projects[0]
        post_data = dict(title="Update title", description="Update description", type="back-end")
        response = self.client.put(f'/api/projects/{project.id}', data=post_data,HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)


    def test_update_project_not_contributor(self):
        self.client.force_login(user=self.notcontributor)
        tokens = RefreshToken.for_user(self.notcontributor)
        access_token = str(tokens.access_token)
        project = self.projects[0]
        post_data = dict(title="Update title", description="Update description", type="back-end")
        response = self.client.put(f'/api/projects/{project.id}', data=post_data, HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.content)


    def test_delete_project_unauthenticated(self):
        access_token = ""
        project = Project.objects.create()
        project = self.projects[0]
        response = self.client.delete(f'/api/projects/{project.id}', HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, response.content)



    def test_delete_project(self):
        self.client.force_login(user=self.users[0])
        tokens = RefreshToken.for_user(self.users[0])
        access_token = str(tokens.access_token)
        project = self.projects[0]
        response = self.client.delete(f'/api/projects/{project.id}', HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, response.content)


    def test_delete_project_not_contributor(self):
        self.client.force_login(user=self.users[2])
        tokens = RefreshToken.for_user(self.users[2])
        access_token = str(tokens.access_token)
        project = self.projects[0]
        response = self.client.delete(f'/api/projects/{project.id}', HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.content)


    def test_list_contributors_unauthenticated(self):
        access_token = ""
        project = Project.objects.create()
        Contributor.objects.create(project_id=project, user_id=self.users[0])
        response = self.client.get(f'/api/projects/{project.id}/users/', HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, response.content)

    def test_list_contributors(self):
        self.client.force_login(user=self.users[0])
        tokens = RefreshToken.for_user(self.users[0])
        access_token = str(tokens.access_token)
        project = Project.objects.create()
        Contributor.objects.create(project_id=project, user_id=self.users[0])
        response = self.client.get(f'/api/projects/{project.id}/users/', HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)


