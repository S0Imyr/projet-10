from django.shortcuts import render, get_object_or_404
from django.http import Http404

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, generics, mixins

from.serializers import ProjectSerializer, IssueSerializer, CommentSerializer, ContributorSerializer
from .models import Project, Issue, Comment, Contributor
from authentication.models import User

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


class ProjectDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    """
    Retrieve, update or delete a project instance
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthor]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ProjectUsersList(APIView, IsContributor):
    """
    List all users for a given project(pk), or create a new user for a given project(pk)
    """
    permission_classes = [IsContributor]

    def get(self, request, pk, format=None):
        contributors = Contributor.objects.filter(project_id=pk)
        serializer = ContributorSerializer(contributors, many=True)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        if int(request.data['project_id']) == pk:
            serializer = ContributorSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            Response(status=status.HTTP_401_UNAUTHORIZED)


class ProjectUserDelete(APIView, IsContributor):
    permission_classes = [IsContributor]
    
    def get_object(self, pk1, pk2):
        try:
            project = get_object_or_404(Project, pk=pk1)
            user = get_object_or_404(User, pk=pk2)
            return Contributor.objects.get(user_id=user, project_id=project)
        except Contributor.DoesNotExist:
            raise Http404

    def delete(self, request, pk1, pk2, format=None):
        contributor = self.get_object(pk1, pk2)
        contributor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProjectIssuesList(APIView, IsContributor):
    permission_classes = [IsContributor]

    def get(self, request, pk, format=None):
        issues = Issue.objects.filter(project_id=pk)
        serializer = IssueSerializer(issues, many=True)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        if int(request.data['project_id']) == pk:
            serializer = IssueSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            Response(status=status.HTTP_401_UNAUTHORIZED)


class ProjectIssueModify(APIView):
    """ IsIssueAuthor """
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


class IssueCommentsList(APIView, IsContributor):
    permission_classes = [IsContributor]
    def get(self, request, format=None):
        pass

    def post(self, request, format=None):
        pass


class IssueCommentDetail(APIView):
    """ IsCommentAuthor """
    def get(self, request, format=None):
        pass

    def put(self, request, format=None):
        pass

    def delete(self, request, format=None):
        pass
