from django.urls import include, path
from rest_framework import routers

from . import views


urlpatterns = [
    path('', views.apiOverview, name='api-overview'),
    path('projects/', views.ProjectList.as_view(), name='project-list'),
    path('projects/<str:pk>', views.ProjectDetail.as_view(), name='project-details'),

]