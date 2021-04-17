from django.urls import include, path
from rest_framework import routers

from . import views


urlpatterns = [
    path('', views.apiOverview, name='api-overview'),
    path('signup/', views.Register.as_view(), name=register)
    path('login/', views.Login.as_view(), name=login)
    path('projects/', views.ProjectsList.as_view(), name='projects-list'),
    path('projects/<str:pk>', views.ProjectDetail.as_view(), name='project-details'),
    path('/projects/<str:pk>/users/', views.ProjectUsersList.as_view(), name='project-users-list'),
    path('/projects/<str:pk>/users/<str:pk>', views.ProjectUserDelete.as_view(), name='delete-project-user'),
    path('/projects/<str:pk>/issues/', views.ProjectIssuesList.as_view(), name='project-issues-list'),
    path('/projects/<str:pk>/issues/<str:pk>', views.ProjectIssueModify.as_view(), name='project-issue-modify'),
    path('/projects/<str:pk>/issues/<str:pk>/comments/', views.IssueCommentsList.as_view(), name='issue-comments-list'),
    path('/projects/<str:pk>/issues/<str:pk>/comments/<str:pk>', views.IssueCommentDetail.as_view(), name='issue-comment-detail'),
]