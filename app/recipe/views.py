from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
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

    # defining a common private functions

    def _params_to_ints(self, qs):
        """ Convert a list of String IDs to a list of integers """
        return [int(str_id) for str_id in qs.split(',')]

    # http://127.0.0.1:8000/api/recipe/recipes/?ingredients=3&tags=1
    def get_queryset(self):
        """ retrieve the recipes for the authenticated user """
        tags = self.request.query_params.get('tags')
        # if no tags provided get function returns None
        ingredients = self.request.query_params.get('ingredients')
        queryset = self.queryset

        if tags:
            tag_ids = self._params_to_ints(tags)
            queryset = queryset.filter(tags__id__in=tag_ids)
            # this is the django syntax for filtering on foreignkey objects
        if ingredients:
            ingredient_ids = self._params_to_ints(ingredients)
            queryset = queryset.filter(ingredients__id__in=ingredient_ids)

        return queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        """ return appoperiate serializer class """
        if self.action == 'retrieve':
            return serializers.RecipeDetailSerializer
        elif self.action == 'upload_image':
            return serializers.RecipeImageSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        """ create a new recipe for authenticated user """
        serializer.save(user=self.request.user)

    # the detail url containing id
    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """ upload an image to a recipe """
        # the object that is accessed based on the id
        recipe = self.get_object()
        serializer = self.get_serializer(
            recipe,
            data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
