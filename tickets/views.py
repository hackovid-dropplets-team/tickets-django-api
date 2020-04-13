from rest_framework import viewsets, mixins
from . import serializers, models, permissions
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import F, Func
from django.db.models import Q


class TicketsViewSet(viewsets.ModelViewSet):
    queryset = models.Ticket.objects.all()
    serializer_class = serializers.TicketSerializer
    permission_classes = [permissions.IsOwnerOrReadOnly]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['owner'] = request.user
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = models.Ticket.objects.all()
        order_by = ['-published']
        zip_code = self.request.query_params.get('zip', None)
        if zip_code is not None:
            queryset = queryset.annotate(
                score=(
                    Func(
                        (F('zip_code') - zip_code),
                        function='ABS'
                    )
                ))
            order_by = ['score', *order_by]
        iam_owner = self.request.query_params.get('iamOwner', False)
        if iam_owner:
            queryset = queryset.filter(owner=self.request.user)
        return queryset.order_by(*order_by)


class DialogViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    queryset = models.Dialog.objects.all()
    serializer_class = serializers.DialogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return models.Dialog.objects.filter(Q(ticket__owner=self.request.user) | Q(voluntary=self.request.user))

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['ticket'] = models.Ticket.objects.get(
            pk=request.data['ticket']['id'])
        serializer.validated_data['voluntary'] = request.user
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
