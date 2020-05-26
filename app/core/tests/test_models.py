from django.test import TestCase
from django.contrib.auth import get_user_model
from unittest.mock import patch
from core import models


def sample_user(email='test@eniac.com', password='testpass'):
    """ Create a Sample User """
    return get_user_model().objects.create_user(email, password)

class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """ Test creating a new user with an email successful """
        email = "test@eniac.com"
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """test the email with a new user normalized"""
        email = "test@ENIAC.com"
        user = get_user_model().objects.create_user(
            email=email,
            password='TEST123',
        )

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """ Test Creating user with No email filled"""
        with self.assertRaises(ValueError):
            """ what is written here should raise ValueError"""
            get_user_model().objects.create_user(None, 'Test123')

    def test_creating_new_super_user(self):
        """ Test creating a new super user with django command line"""
        user = get_user_model().objects.create_superuser(
            email='p.zakery@hotmail.com',
            password='super123'
        )

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        # included as a part of PermissionsMixin

    def test_tag_str(self):
        """ test the tag string representation """
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan',
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """ test the ingredient string representation """
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name='Cucumber',
        )

        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """ test the recipe string representation"""
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title='steak and mushroom sauce',
            time_minutes=5,
            price=5.00,
        )

        self.assertEqual(str(recipe), recipe.title)

    # refer to session 70
    @patch('uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """ test that image is saved in the correct location """
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, 'myimage.jpg')
        # None is for instance

        exp_path = f'uploads/recipe/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)
