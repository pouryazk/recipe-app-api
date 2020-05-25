from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):

    def setUp(self):  # is triggered before any tests in the class
        self.client = Client()  # docs are included in the folder documentation
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@eniac.com',
            password="password123",
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='test@eniac.com',
            password="password123",
            name="test user full name",
        )

    def test_user_listed(self):
        """ tests that users are listed in the users page"""
        url = reverse('admin:core_user_changelist')  # making dynamic url
        # response
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)  # resources are included

    def test_user_change_page(self):
        """ Test that user edit page works"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        # /admin/core/user/<id>
        res = self.client.get('url')

        self.assertEqual(res.status_code, 200)
        # status code for ok

    def test_create_user_page(self):
        """ test that create user page works """
        url = reverse('admin:core_user_add')
        res = self.client.get('url')

        self.assertEqual(res.status_code, 200)
"""
    def test_admin_itself(self):
        url = '/admin'
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
"""
