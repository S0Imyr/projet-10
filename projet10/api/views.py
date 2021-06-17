from django.shortcuts import render, get_object_or_404
from django.http import Http404

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers, status, generics, mixins

from.serializers import ProjectSerializer, IssueSerializer, CommentSerializer, ContributorSerializer
from .models import Project, Issue, Comment, Contributor
from authentication.models import User
from authentication.serializers import UserSerializer

from .permissions import IsContributor, IsAuthor


@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'Projects list (GET) and Create project (POST)': '/projects/',
        'Get project details  (GET), Update (PUT) and Delete (DELETE) a project': '/projects/<str:pk>',
        'Users list (GET) and Add a user to a project (POST)': '/projects/<str:pk>/users/',
        'Delete a user from a project (DELETE)': '/projects/<str:pk>/users/<str:pk>',
        'Issues list for a project (GET) and Create an issue for a project (POST)': '/projects/<str:pk>/issues/',
        'Update (PUT) and Delete (DELETE) an issue for a project (PUT)': '/projects/<str:pk>/issues/<str:pk>',
        'Comments List for an issue (GET) and Create comment about an issue (POST)': '/projects/<str:pk>/issues/<str:pk>/comments/',
        'Update (PUT) and Delete (DELETE) a comment ': '/projects/<str:pk>/issues/<str:pk>/comments/<str:pk>',
        'Get a comments with its id (GET)': '/projects/<str:pk>/issues/<str:pk>/comments/<str:pk>',
    }
    return Response(api_urls)


class ProjectsList(generics.ListCreateAPIView):
    """
    List all projects, or create a new project
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_queryset(self):
        """Select projects where the user is involved"""
        contributions = Contributor.objects.filter(user_id=self.request.user)
        contributed_projects_id = []
        for contribution in contributions:
            contributed_projects_id.append(contribution.project_id.id)
        return Project.objects.filter(id__in=contributed_projects_id)

    def perform_create(self, serializer):
        """
        Save the project with the user as author.
        Create a Contributor link between the new project and the author user.
        """
        project = serializer.save(author_user_id=self.request.user)
        Contributor.objects.create(user_id=self.request.user, project_id=project, permission='allowed', role='author')


class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a project instance
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthor]

    def get_object(self, *args, **kwargs):
        project_pk = int(self.kwargs["project_pk"])
        project = get_object_or_404(Project, pk=project_pk)
        self.check_object_permissions(self.request, project)
        return project



class ProjectUsersList(generics.ListCreateAPIView):
    """
    List all users for a given project, or create a new user for a given project
    """
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    permission_classes = [IsContributor]

    def get_queryset(self, *args, **kwargs):
        project = kwargs.get("project_pk")
        return Contributor.objects.filter(project_id=project)

    def perform_create(self, serializer, *args, **kwargs):
        project_pk = self.kwargs['project_pk']
        project = Project.objects.get(pk=project_pk)
        serializer.save(project_id=project)


class ProjectUserDelete(generics.DestroyAPIView):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthor]
    

    def get_object(self):
        queryset = self.get_queryset()
        project_pk = self.kwargs["project_pk"]
        user_pk = self.kwargs["user_pk"]
        project = get_object_or_404(Project, pk=project_pk)
        user = get_object_or_404(User, pk=user_pk)
        filter = {'project_id': project, 'user_id': user}
        contributor = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, project)
        return contributor


class ProjectIssuesList(generics.ListCreateAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IsContributor]

    def get_queryset(self, *args, **kwargs):
        project = self.kwargs.get("project_pk")
        return Issue.objects.filter(project_id=project)

    def perform_create(self, serializer, *args, **kwargs):
        project_pk = self.kwargs['project_pk']
        project = Project.objects.get(pk=project_pk)
        serializer.save(project_id=project)


class ProjectIssueModify(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthor]
    def put(self, request, pk1, pk2, format=None):
        project_issues = Issue.objects.filter(project_id=pk1)
        project_issue = project_issues.get(pk=pk2)
        serializer = IssueSerializer(instance=project_issue, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk1, pk2, format=None):
        project_issues = Issue.objects.filter(project_id=pk1)
        project_issue = project_issues.get(pk=pk2)
        project_issue.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class IssueCommentsList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsContributor]

    def get_queryset(self, *args, **kwargs):
        project = self.kwargs.get("project_pk")
        return Issue.objects.filter(project_id=project)

    def perform_create(self, serializer, *args, **kwargs):
        project_pk = self.kwargs['project_pk']
        project = Project.objects.get(pk=project_pk)
        serializer.save(project_id=project)


class IssueCommentDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthor]
    def get(self, request, format=None):
        pass

    def put(self, request, format=None):
        pass

    def delete(self, request, format=None):
        pass
