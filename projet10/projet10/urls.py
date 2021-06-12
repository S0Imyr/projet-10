
from django.contrib import admin
from django.urls import path, include
from django.urls import include, path

from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from authentication import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include("api.urls")),
    path('api/', include("authentication.urls")),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Utils
    path('api/users', views.UsersList.as_view(), name='users-list'),

    # Temp
    path('api/logout/', views.Logout.as_view(), name='logout'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
