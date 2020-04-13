from rest_framework import serializers
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.fields import empty

from .models import Ticket, Dialog


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class TicketSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    is_owner = serializers.SerializerMethodField(read_only=True)
    chat_id = serializers.SerializerMethodField(read_only=True)
    requires_context = True

    class Meta:
        model = Ticket
        depth = 1
        fields = '__all__'

    def get_is_owner(self, value):
        return value.owner.id == self.context['request'].user.id

    def get_chat_id(self, value):
        try:
            dialog = Dialog.objects.get(
                ticket=value, voluntary=self.context['request'].user.id)
            return dialog.id
        except ObjectDoesNotExist:
            return None


class DialogSerializer(serializers.ModelSerializer):
    ticket = TicketSerializer(read_only=True)
    voluntary = UserSerializer(read_only=True)

    class Meta:
        model = Dialog
        fields = '__all__'
