from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response

from.serializers import ProjectSerializer
from .models import Project


@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'Projects list (GET)': '/projects/',
        'Create project (POST)': '/projects/',
        'Get project details  (GET)': '/projects/<str:pk>',
        'Update a project (PUT)': '/projects/<str:pk>',
        'Delete a project (DELETE)': '/projects/<str:pk>',
        'Add a user to a project (POST)': '/projects/<str:pk>/users/',
        'Get the list of users of a project(GET)': '/projects/<str:pk>/users/',
        'Delete a user from a project (DELETE)': '/projects/<str:pk>/users/<str:pk>',
        'Get the list of issues for a project (GET)': '/projects/<str:pk>/issues/',
        'Create an issue for a project (POST)': '/projects/<str:pk>/issues/',
        'Update an issue for a project (PUT)': '/projects/<str:pk>/issues/<str:pk>',
        'Delete an issue for a project (DELETE)': '/projects/<str:pk>/issues/<str:pk>',
        'Create comment about an issue (POST)': '/projects/<str:pk>/issues/<str:pk>/comments/',
        'Get the list of comments for an issue (GET)': '/projects/<str:pk>/issues/<str:pk>/comments/',
        'Update a comments (PUT)': '/projects/<str:pk>/issues/<str:pk>/comments/<str:pk>',
        'Delete a comments (DELETE)': '/projects/<str:pk>/issues/<str:pk>/comments/<str:pk>',
        'Get a comments with its id (GET)': '/projects/<str:pk>/issues/<str:pk>/comments/<str:pk>',
    }
    return Response(api_urls)


@api_view(['GET'])
def get_projects_list(request):
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def create_project(request):
    pass


@api_view(['GET'])
def get_project_details(request):
    pass


@api_view(['PUT'])
def update_project(request):
    pass


@api_view(['DELETE'])
def delete_project(request):
    pass


@api_view(['POST'])
def add_user_to_project(request):
    pass


@api_view(['GET'])
def get_users_list_on_project(request):
    pass


@api_view(['POST'])
def create_project(request):
    pass


@api_view(['DELETE'])
def delete_user_from_project(request):
    pass


@api_view(['GET'])
def get_issues_list_for_project(request):
    pass


@api_view(['POST'])
def create_issue_for_project(request):
    pass


@api_view(['PUT'])
def update_issue_project(request):
    pass


@api_view(['DELETE'])
def delete_issue_project(request):
    pass


@api_view(['POST'])
def create_comment_for_issue(request):
    pass


@api_view(['GET'])
def get_comments_list_for_issue(request):
    pass


@api_view(['POST'])
def create_issue_for_project(request):
    pass


@api_view(['PUT'])
def update_comment(request):
    pass


@api_view(['DELETE'])
def delete_comment(request):
    pass


@api_view(['GET'])
def get_comment_by_id(request):
    pass
