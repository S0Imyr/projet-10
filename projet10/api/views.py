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
        'Get the details of project (GET)': '/projects/<str:pk>',
        'Update a project (PUT)': '/projects/<str:pk>',
        'Delete a project (DELETE)': '/projects/<str:pk>',
        'Add a user to a project (POST)': '/projects/<str:pk>/users/',
        'Get the list of users on a project(GET)': '/projects/<str:pk>/users/',
        'Delete a user from a project (DELETE)': '/projects/<str:pk>/users/<str:pk>',
        'Get the list of issues on a project (GET)': '/projects/<str:pk>/issues/',
        'Create an issue on a project (POST)': '/projects/<str:pk>/issues/',
        'Update an issue on a project (PUT)': '/projects/<str:pk>/issues/<str:pk>',
        'Delete an issue on a project (DELETE)': '/projects/<str:pk>/issues/<str:pk>',
        'Create comment about an issue (POST)': '/projects/<str:pk>/issues/<str:pk>/comments/',
        'Get the list of comments about an issue (GET)': '/projects/<str:pk>/issues/<str:pk>/comments/',
        'Update a comments (PUT)': '/projects/<str:pk>/issues/<str:pk>/comments/<str:pk>',
        'Delete a comments (DELETE)': '/projects/<str:pk>/issues/<str:pk>/comments/<str:pk>',
        'Get a comments with its id (GET)': '/projects/<str:pk>/issues/<str:pk>/comments/<str:pk>',
    }
    return Response(api_urls)

@api_view(['GET'])
def project_list(request):
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)