from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class AuthUserViewSet(viewsets.ViewSet):

  @action(methods=['post'], detail=False, url_path='login-user', url_name='login_user')
  def login(self, request, pk=None):

    email = request.data['email']
    password = request.data['password']

    user_auth = User.objects.filter(email=email)
    print(user_auth)

    return Response(user_auth)
