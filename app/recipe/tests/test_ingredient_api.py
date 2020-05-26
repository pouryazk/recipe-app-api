from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient
from recipe.serializers import IngredientSerializer


INGREDIENTS_URL = reverse('recipe:ingredient-list')


class PublicIngredientApiTest(TestCase):
    """ Test the publicly available ingredients API """

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """ tests that login is required to access endpoint """
        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientApiTest(TestCase):
    """ Test Private ingredients API """

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@eniac.com',
            'testpass',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredient_list(self):
        """ Tests retrieving a list of ingredients """
        Ingredient.objects.create(user=self.user, name='KALE')
        Ingredient.objects.create(user=self.user, name='Salt')

        res = self.client.get(INGREDIENTS_URL)
        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        """test that ingredients for the authenticated user are returned"""
        user2 = get_user_model().objects.create_user(
            'test2@eniac.com',
            'testpass123',
        )
        Ingredient.objects.create(
            user=user2,
            name='vinegar',
        )
        ingredients = Ingredient.objects.create(
            user=self.user,
            name='Tumeric',
        )

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredients.name)

    def test_create_ingredient_successful(self):
        """ test create a new ingredient """
        payload = {
            'name':'cabbage'
        }
        self.client.post(INGREDIENTS_URL, payload)

        exists = Ingredient.objects.filter(
            user=self.user,
            name=payload['name'],
        ).exists()

        self.assertTrue(exists)

    def test_create_ingredient_invalid(self):
        """ test creating invalid ingredients failure """
        payload = {
            'name':""
        }
        res = self.client.post(INGREDIENTS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
          