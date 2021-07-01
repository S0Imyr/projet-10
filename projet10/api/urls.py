from django.urls import path

from . import views


urlpatterns = [
    path('', views.apiOverview, name='api-overview'),
    path('projects/', views.ProjectsList.as_view(), name='projects-list'),
    path('projects/<str:project_pk>', views.ProjectDetail.as_view(), name='project-details'),
    path('projects/<str:project_pk>/users/', views.ProjectUsersList.as_view(), name='project-users-list'),
    path('projects/<str:project_pk>/users/<str:user_pk>',
        views.ProjectUserDelete.as_view(), name='delete-project-user'),
    path('projects/<str:project_pk>/issues/', views.ProjectIssuesList.as_view(), name='project-issues-list'),
    path(
        'projects/<str:project_pk>/issues/<str:issue_pk>',
        views.ProjectIssueModify.as_view(), name='project-issue-modify'),
    path(
        'projects/<str:project_pk>/issues/<str:issue_pk>/comments/',
        views.IssueCommentsList.as_view(), name='issue-comments-list'),
    path(
        'projects/<str:project_pk>/issues/<str:issue_pk>/comments/<str:comment_pk>',
        views.IssueCommentDetail.as_view(), name='issue-comment-detail'),
]
