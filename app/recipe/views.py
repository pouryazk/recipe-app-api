from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Ingredient, Recipe
from recipe import serializers


class BaseRecipeAttrViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin,
                            ):
      """Base Viewset for user owned recipe attributes"""
      authentication_classes = [TokenAuthentication]
      permission_classes = [IsAuthenticated]

      def get_queryset(self):  # this will be displayed on the api
          """ return objects for the current authenticated user only """
          return self.queryset.filter(user=self.request.user).order_by('-name')

      def perform_create(self, serializer):  # perform any modification to create
          """ create a new attr """
          serializer.save(user=self.request.user)


class TagViewSet(BaseRecipeAttrViewSet):
    # link is available in the resources for the docs
    """ Manage Tag in the Database """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # list model requires queryset
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class IngredientViewSet(BaseRecipeAttrViewSet):
      """ Manage ingredients in the database """
      queryset = Ingredient.objects.all()
      serializer_class = serializers.IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """ manage recipes in the database """
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """ retrieve the recipes for the authenticated user """
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        """ return appoperiate serializer class """
        if self.action == 'retrieve':
            return serializers.RecipeDetailSerializer

        return self.serializer_class
