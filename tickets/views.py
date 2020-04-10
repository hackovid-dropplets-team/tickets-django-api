from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from django.http import HttpResponse
from django.http import JsonResponse

import json

from . import serializers
from . import models
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics


class TicketsViewSet(viewsets.ModelViewSet):
    queryset = models.Ticket.objects.all().order_by('name')
    serializer_class = serializers.TicketSerializer


class VolunteeringViewSet(viewsets.ModelViewSet):
    queryset = models.Volunteering.objects.all()
    serializer_class = serializers.VolunteeringSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


@api_view(['POST'])
def create_auth(request):
    serialized = serializers.UserSerializer(
        data=request.data, context={'request': request})

    if serialized.is_valid():
        User.objects.create_user(
            serialized.data['email'],
            serialized.data['username'],
            serialized.data['password']
        )
        return Response(serialized.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)


class HelloView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello world'}
        return Response(content)
