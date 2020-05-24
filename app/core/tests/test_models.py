from django.test import TestCase
from django.contrib.auth import get_user_model


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
