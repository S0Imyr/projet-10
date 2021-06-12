from django.urls import path

from . import views

urlpatterns = [
    path('signup/', views.Register.as_view(), name='register'),
    # Utils
    path('users/', views.UsersList.as_view(), name='users-list'),
]



    
    