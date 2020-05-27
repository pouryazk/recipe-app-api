from rest_framework import serializers
from core.models import Tag, Ingredient, Recipe


class TagSerializer(serializers.ModelSerializer):
    """ serializer for tag object """

    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']


class IngredientSerializer(serializers.ModelSerializer):
    """ Serializer for ingredient object """

    class Meta:
        model = Ingredient
        fields = ('id', 'name')
        read_only_fields = ['id']


class RecipeSerializer(serializers.ModelSerializer):
    """ serialize the recipe model """
    ingredients = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Ingredient.objects.all(),
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    # read the PrimaryKeyRelatedField docs included in 63th session


    class Meta:
        model = Recipe
        fields = ('id', 'title', 'ingredients',
                  'tags', 'time_minutes', 'price'
                 )
        read_only_fields = ('id',)
        # prevent the user from updating the id

class RecipeDetailSerializer(RecipeSerializer):
    """ Serialize a recipe detail """
    ingredients = IngredientSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)


class RecipeImageSerializer(serializers.ModelSerializer):
    """ serializer for uploading images to recipies """

    class Meta:
        model = Recipe
        fields = ('id','image')
        read_only_fields = ('id',)
