from rest_framework import serializers
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.fields import empty

from .models import Ticket, Volunteering


class VolunteeringSerializer(serializers.ModelSerializer):
    class Meta:
        model = Volunteering
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class TicketSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Ticket
        fields = '__all__'
