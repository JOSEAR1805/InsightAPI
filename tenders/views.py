from django.shortcuts import render
from rest_framework import routers, serializers, viewsets
from .models import Tender, TenderSerializer

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, authentication
from django.http import HttpResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


# Create your views here.


class TenderViewSet(viewsets.ModelViewSet, authentication.BaseAuthentication):
    queryset = Tender.objects.all()
    serializer_class = TenderSerializer
    """
    Authentication is needed for this methods
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @action(methods=['get'], detail=False, url_path='tender-users', url_name='tender-users')
    def tenderUsers(self, request, pk=None):
        print(request.user, request.auth, '*' * 10)
        return Response('ERROR CON LOS DATOS', status=status.HTTP_400_BAD_REQUEST)
