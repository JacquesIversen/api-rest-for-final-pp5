from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile, Issue
from django.db.models.signals import post_save
from django.test.utils import override_settings
from rest_framework.test import APITestCase
from rest_framework import status

def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(owner=instance)

class ProfileModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.signal_was_called = False

        # Connect the signal to the test receiver function
        post_save.connect(self.handle_post_save, sender=User)

    def tearDown(self):
        # Disconnect the signal after the test
        post_save.disconnect(self.handle_post_save, sender=User)

    def handle_post_save(self, sender, instance, **kwargs):
        # Check if the signal was called with the correct arguments
        if sender == User and isinstance(instance.profile, Profile):
            self.signal_was_called = True

    def test_profile_creation(self):
        # Test if a new profile is created when a user is created
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertIsInstance(self.user.profile, Profile)

    def test_signal_triggered(self):
        # Test if the signal triggers the creation of a profile
        new_user = User.objects.create_user(username='testuser2', password='testpassword')
        self.assertTrue(self.signal_was_called)
        self.assertTrue(hasattr(new_user, 'profile'))
        self.assertIsInstance(new_user.profile, Profile)





""" Test for Issues.View """

class IssueViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.url = '/issue/'  # Update this URL based on your project's URL configuration

    def test_create_issue(self):
        # Ensure a user can create an issue
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'Test Issue',
            'car': 'Test Car',
            'model': 'Test Model',
            'year': 2022,
            'engine_size': '2.0L',
            'description': 'This is a test issue description.'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Issue.objects.count(), 1)

    def test_list_issues(self):
        # Ensure issues can be listed
        Issue.objects.create(title='Issue 1', owner=self.user, car='Car 1', description='Description 1')
        Issue.objects.create(title='Issue 2', owner=self.user, car='Car 2', description='Description 2')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_filter_and_order_issues(self):
        # Ensure issues can be filtered and ordered
        Issue.objects.create(title='Car A Issue', owner=self.user, car='Car A', description='Description 1')
        Issue.objects.create(title='Car B Issue', owner=self.user, car='Car B', description='Description 2')
        self.client.force_authenticate(user=self.user)

        # Test filtering by car and ordering by title
        response = self.client.get(self.url, {'search': 'Car A', 'ordering': 'title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['car'], 'Car A')

        # Test ordering by description
        response = self.client.get(self.url, {'ordering': 'description'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['description'], 'Description 1')

    def test_issue_owner_is_authenticated_user(self):
        # Ensure the owner of the issue is the authenticated user
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'Test Issue',
            'car': 'Test Car',
            'model': 'Test Model',
            'year': 2022,
            'engine_size': '2.0L',
            'description': 'This is a test issue description.'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['owner'], self.user.id)