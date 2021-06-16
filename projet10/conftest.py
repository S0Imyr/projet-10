import pytest
import random

from api.models import Project, Contributor, Issue, Comment, \
                        CONTRIBUTOR_PERMISSION_CHOICES, PROJECT_TYPE_CHOICES, \
                        ISSUE_PRIORITY_CHOICES, ISSUE_TAG_CHOICES, ISSUE_STATUS_CHOICES
from authentication.models import User


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


@pytest.fixture(scope="session")
def environnement(db, new_user_factory, new_project_factory):
    user1 = new_user_factory("UserTest1", "test1@test.com", "password1", "Name1")
    user2 = new_user_factory("UserTest2", "test2@test.com", "password2", "Name2")
    user3 = new_user_factory("UserTest3", "test3@test.com", "password3", "Name3")
    user4 = new_user_factory("UserTest4", "test4@test.com", "password4", "Name4")
    users = [user1, user2, user3, user4]

    project1 = new_project_factory("Projet1", user1)
    project2 = new_project_factory("Projet2", user2)
    project3 = new_project_factory("Projet3", user3)
    project4 = new_project_factory("Projet4", user4)
    projects = [project1, project2, project3, project4]

    return users, projects 
    
