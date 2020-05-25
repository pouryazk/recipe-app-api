from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag
from recipe import serializers


class TagViewSet(viewsets.GenericViewSet,
                 mixins.ListModelMixin,
                 mixins.CreateModelMixin,
                 ):
    # link is available in the resources for the docs
    """ Manage Tag in the Database """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # list model requires queryset
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer

    def get_queryset(self):  # this will be displayed on the api
        """ return objects for the current authenticated user only """
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):  # perform any modification to create
        """ create a new tag """
        serializer.save(user=self.request.user)
