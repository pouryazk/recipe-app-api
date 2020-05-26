from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag

from recipe.serializers import TagSerializer

TAGS_URL = reverse('recipe:tag-list')  # because of the usage of viewsets


class PublicTagsApiTest(TestCase):
    """ test the publicly available tags api """

    def setUp(self):
        self.client= APIClient()

    def test_login_required(self):
        """Tests that login is required for retrieving tags"""
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateTagsApiTests(TestCase):
    """ Test the authorized user tag api """

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@eniac.com',
            'password123',
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """ test retrieving tags """
        Tag.objects.create(user=self.user, name='Vegen')
        Tag.objects.create(user=self.user, name='Dessert')

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)  # Many must be included

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """ Tests that tags returned are for authenticated user """
        user2 = get_user_model().objects.create_user(
            'paze@eniac.com',
            'testpass',
        )
        Tag.objects.create(user=user2, name='Fruity')
        tag = Tag.objects.create(user=self.user, name='Comfort Food')

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)

    def test_create_tag_successful(self):
        """ test creating a new tag """
        payload = {
            'name':'Test Tag'
        }

        self.client.post(TAGS_URL, payload)

        exists = Tag.objects.filter(
            user=self.user,
            name=payload['name'],
        ).exists()  # returns a boolean

        self.assertTrue(exists)

    def test_create_tag_invalid(self):
        """ tests creating a new tag with invalid payload"""
        payload = {'name':""}
        res = self.client.post(TAGS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)