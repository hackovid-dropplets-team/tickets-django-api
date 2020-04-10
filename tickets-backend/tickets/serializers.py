from rest_framework import serializers
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.fields import empty

from .models import Ticket, Volunteering


class TicketSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'


class VolunteeringSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Volunteering
        fields = '__all__'


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']
