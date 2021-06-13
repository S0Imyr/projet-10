from django.urls import include, path

from . import views


urlpatterns = [
    path('', views.apiOverview, name='api-overview'),
    
    path('projects/', views.ProjectsList.as_view(), name='projects-list'),
    path('projects/<str:pk>', views.ProjectDetail.as_view(), name='project-details'),
    path('projects/<str:pk>/users/', views.ProjectUsersList.as_view(), name='project-users-list'),
    path('projects/<str:pk1>/users/<str:pk2>', views.ProjectUserDelete.as_view(), name='delete-project-user'),
    path('projects/<str:pk>/issues/', views.ProjectIssuesList.as_view(), name='project-issues-list'),
    path('projects/<str:pk1>/issues/<str:pk2>', views.ProjectIssueModify.as_view(), name='project-issue-modify'),
    path('projects/<str:pk1>/issues/<str:pk2>/comments/', views.IssueCommentsList.as_view(), name='issue-comments-list'),
    path('projects/<str:pk1>/issues/<str:pk2>/comments/<str:pk3>', views.IssueCommentDetail.as_view(), name='issue-comment-detail'),
]