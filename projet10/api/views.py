from django.shortcuts import render
from django.http import JsonResponse, Http404

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from.serializers import ProjectSerializer
from .models import Project, Issue, Comment, Contributor


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


class ProjectList(APIView):
    """
    List all projects, or create a new project
    """
    def get(self, request, format=None):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ProjectDetail(APIView):
    """
    Retrieve, update or delete a project instance
    """
    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        project = self.get_object(pk)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        project = self.get_object(pk)
        serializer = ProjectSerializer(project, data=request)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        project = self.get_object(pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
