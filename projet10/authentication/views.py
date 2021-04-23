from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAdminUser

from .models import User
from .serializers import UserSerializer, RegisterSerializer


class Register(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class Login(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        if request.user.is_authenticated:
            return redirect('api-overview')
        else:
            username = request.data['username']
            password = request.data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return Response(status=status.HTTP_200_OK)
                else:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)


class Logout(APIView):
    def get(self, request):
        logout(request)
        return redirect('login')


class UsersList(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

