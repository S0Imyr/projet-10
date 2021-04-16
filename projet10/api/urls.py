from django.urls import path
from . import views

urlpatterns = [
    path('', views.apiOverview, name='api-overview'),
    path('projects/', views.get_projects_list, name='project-list'),
]