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
    owner = UserSerializer(read_only=True)
    is_owner = serializers.SerializerMethodField(read_only=True)
    requires_context = True

    class Meta:
        model = Ticket
        depth = 1
        fields = '__all__'

    def get_is_owner(self, value):
        return value.owner.id == self.context['request'].user.id
