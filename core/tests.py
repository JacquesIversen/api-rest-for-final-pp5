from os.path import basename
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile, Issue, Comment, Like, DisLike
from django.utils import timezone
from rest_framework.test import APIClient, APITestCase, APIRequestFactory
from rest_framework import status
from django.contrib.auth import get_user_model
from .serializers import IssueSerializer, CommentSerializer, LikeSerializer, DisLikeSerializer



class ProfileModelTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.profile = Profile.objects.get(owner=self.user)

    def test_profile_creation(self):
        # Check initial profile values
        self.assertEqual(self.profile.name, '')
        self.assertIsNone(self.profile.age)
        self.assertIsNone(self.profile.biography)
        self.assertIsNone(self.profile.owned_cars)
        self.assertIsNone(self.profile.issues_posted)
        self.assertIsNone(self.profile.issues_solved)

        # Check default image path
        expected_default_image_path = 'default_profile_ponhew'
        actual_image_path = basename(self.profile.image.url)
        self.assertEqual(actual_image_path, expected_default_image_path)

        # Check ordering
        self.assertEqual(Profile._meta.ordering, ['-issues_solved'])

        # Check __str__ method
        expected_str = f"{self.user}'s profile"
        self.assertEqual(str(self.profile), expected_str)

    def test_create_profile_signal(self):
        # Check if a profile instance is created when a user is created
        new_user = User.objects.create_user(username='newuser', password='testpassword')
        new_profile = Profile.objects.get(owner=new_user)
        
        # Check if the profile fields match the default values
        self.assertEqual(new_profile.name, '')
        self.assertIsNone(new_profile.age)
        self.assertIsNone(new_profile.biography)
        self.assertIsNone(new_profile.owned_cars)
        self.assertIsNone(new_profile.issues_posted)
        self.assertIsNone(new_profile.issues_solved)
        
        # Check if the profile is associated with the correct user
        self.assertEqual(new_profile.owner, new_user)

        # Check default image path for the new profile
        expected_default_image_path = 'default_profile_ponhew'
        actual_image_path = basename(new_profile.image.url)
        self.assertEqual(actual_image_path, expected_default_image_path)
        
        # Check ordering for the new profile
        self.assertEqual(Profile._meta.ordering, ['-issues_solved'])

        # Check __str__ method for the new profile
        expected_str = f"{new_user}'s profile"
        self.assertEqual(str(new_profile), expected_str)


class IssueModelTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        
        # Create a test issue related to the test user
        self.issue = Issue.objects.create(
            owner=self.user,
            title='Test Issue',
            car='Test Car',
            model='Test Model',
            year=2022,
            engine_size='2.0L',
            description='Test Description',
            is_solved=False
        )

    def test_issue_creation(self):
        # Retrieve the test issue from the database
        issue = Issue.objects.get(id=self.issue.id)
        
        # Check if the issue fields match the values set during setup
        self.assertEqual(issue.owner, self.user)
        self.assertEqual(issue.title, 'Test Issue')
        self.assertEqual(issue.car, 'Test Car')
        self.assertEqual(issue.model, 'Test Model')
        self.assertEqual(issue.year, 2022)
        self.assertEqual(issue.engine_size, '2.0L')
        self.assertEqual(issue.description, 'Test Description')
        self.assertFalse(issue.is_solved)  # Check if is_solved is False
        
        # Check ordering
        self.assertEqual(Issue._meta.ordering, ['-created_at'])
        
        # Check __str__ method
        expected_str = f'{self.issue.id} Test Issue'
        self.assertEqual(str(issue), expected_str)

    def test_default_image_path(self):
        # Check default image path for the test issue
        expected_default_image_path = 'default_post_rgq6aq'
        actual_image_path = basename(self.issue.image.url)
        self.assertEqual(actual_image_path, expected_default_image_path)



class CommentTestCase(TestCase):
    def setUp(self):
        # Create a User
        self.user = User.objects.create(username='testuser')

        # Create an Issue
        self.issue = Issue.objects.create(title='Test Issue', description='Sample description', owner=self.user)

    def test_comment_creation(self):
        # Create a Comment
        comment = Comment.objects.create(
            owner=self.user,
            issue=self.issue,
            comment_area='This is a test comment'
        )

        # Check if the comment was created successfully
        self.assertEqual(comment.owner, self.user)
        self.assertEqual(comment.issue, self.issue)
        self.assertEqual(comment.comment_area, 'This is a test comment')

        # Check if created_at is in the past and not in the future
        self.assertLessEqual(comment.created_at, timezone.now())

    def test_comment_ordering(self):
        # Create comments with different created_at timestamps
        comment1 = Comment.objects.create(owner=self.user, issue=self.issue, comment_area='Comment 1')
        comment2 = Comment.objects.create(owner=self.user, issue=self.issue, comment_area='Comment 2')
        comment3 = Comment.objects.create(owner=self.user, issue=self.issue, comment_area='Comment 3')

        # Check if comments are ordered by created_at in ascending order
        comments = Comment.objects.all()
        self.assertEqual(list(comments), [comment1, comment2, comment3])

    def test_comment_str_method(self):
        comment = Comment.objects.create(owner=self.user, issue=self.issue, comment_area='Test Comment')
        self.assertEqual(str(comment), 'Test Comment')



class LikeModelTest(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        # Create an issue
        self.issue = Issue.objects.create(
            owner=self.user,
            title='Test Issue',
            description='Sample description'
        )
        # Create a comment related to the issue
        self.comment = Comment.objects.create(
            owner=self.user,
            issue=self.issue,
            comment_area='Test Comment'
        )

    def test_like_creation(self):
        # Create a Like object
        like = Like.objects.create(owner=self.user, comment=self.comment)
        
        # Check if the Like object is created successfully
        self.assertEqual(like.owner, self.user)
        self.assertEqual(like.comment, self.comment)
        



class DisLikeModelTest(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        # Create an issue
        self.issue = Issue.objects.create(
            owner=self.user,
            title='Test Issue',
            description='Sample description'
        )
        # Create a comment related to the issue
        self.comment = Comment.objects.create(
            owner=self.user,
            issue=self.issue,
            comment_area='Test Comment'
        )

    def test_dislike_creation(self):
        # Create a DisLike object
        dislike = DisLike.objects.create(owner=self.user, comment=self.comment)
        
        # Check if the DisLike object is created successfully
        self.assertEqual(dislike.owner, self.user)
        self.assertEqual(dislike.comment, self.comment)
        



## Serializers Testing: 
User = get_user_model()

class SerializerTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.issue = Issue.objects.create(owner=self.user, title='Test Issue', car='Test Car', model='Test Model', year=2022, engine_size='2.0L', description='Test Description', is_solved=False)
        self.comment = Comment.objects.create(owner=self.user, issue=self.issue, comment_area='Test Comment')
        self.like = Like.objects.create(owner=self.user, comment=self.comment)
        self.dislike = DisLike.objects.create(owner=self.user, comment=self.comment)

        # Create a request factory and request object for testing
        self.factory = APIRequestFactory()
        self.request = self.factory.get('/')

        # Assign the user to the request object to simulate an authenticated user
        self.request.user = self.user

    def test_issue_serializer(self):
        serializer = IssueSerializer(instance=self.issue, context={'request': self.request})
        self.assertEqual(serializer.data['id'], self.issue.id)
        self.assertEqual(serializer.data['owner'], self.user.username)
        self.assertEqual(serializer.data['is_owner'], True)  # Assuming the request.user is the owner
        # Add more assertions based on your serializer fields and model fields

    def test_comment_serializer(self):
        serializer = CommentSerializer(instance=self.comment, context={'request': self.request})
        self.assertEqual(serializer.data['id'], self.comment.id)
        self.assertEqual(serializer.data['owner'], self.user.username)
        self.assertEqual(serializer.data['is_owner'], True)  # Assuming the request.user is the owner
        # Add more assertions based on your serializer fields and model fields

    def test_like_serializer(self):
        serializer = LikeSerializer(instance=self.like, context={'request': self.request})
        self.assertEqual(serializer.data['id'], self.like.id)
        self.assertEqual(serializer.data['owner'], self.user.username)
        # Add more assertions based on your serializer fields and model fields

    def test_dislike_serializer(self):
        serializer = DisLikeSerializer(instance=self.dislike, context={'request': self.request})
        self.assertEqual(serializer.data['id'], self.dislike.id)
        self.assertEqual(serializer.data['owner'], self.user.username)
        # Add more assertions based on your serializer fields and model fields


## Views testcases: 

from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from core.models import Issue

class IssueViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.url = '/issue/'

    def test_create_issue(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'Test Issue',
            'description': 'This is a test issue description.',
            # Include other required fields as well
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Issue.objects.count(), 1)
        self.assertEqual(Issue.objects.get().title, 'Test Issue')

    def test_list_issues(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class IssueDetailTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.issue = Issue.objects.create(title='Test Issue', description='Test Description', owner=self.user)
        self.url = f'/issue/{self.issue.id}/'

    def test_retrieve_issue(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_issue(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'Updated Test Issue',
            'description': 'Updated description.',
            # Include other fields you want to update
        }
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Issue.objects.get(id=self.issue.id).title, 'Updated Test Issue')

    def test_delete_issue(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Issue.objects.count(), 0)


class CommentListTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.issue = Issue.objects.create(title='Test Issue', description='Test Description', owner=self.user)
        self.url = '/comments/'

    def test_create_comment(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'issue': self.issue.id,
            'comment_area': 'Test Comment',
            # Include other required fields as well
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.get().comment_area, 'Test Comment')

    def test_list_comments(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CommentDetailTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.issue = Issue.objects.create(title='Test Issue', description='Test Description', owner=self.user)
        self.comment = Comment.objects.create(issue=self.issue, owner=self.user, comment_area='Test Comment')
        self.url = f'/comments/{self.comment.id}/'

    def test_retrieve_comment(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_comment(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'comment_area': 'Updated Test Comment',
            # Include other fields you want to update
        }
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Comment.objects.get(id=self.comment.id).comment_area, 'Updated Test Comment')

    def test_delete_comment(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 0)





from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from core.models import Issue, Comment, Like, DisLike

class LikeDisLikeTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create users
        self.user1 = User.objects.create_user(username='user1', password='password1')
        self.user2 = User.objects.create_user(username='user2', password='password2')

        # Create an issue
        self.issue = Issue.objects.create(
            owner=self.user1,
            title='Test Issue',
            car='Test Car',
            model='Test Model',
            year=2022,
            engine_size='2.0L',
            description='Test Description'
        )

        # Create a comment
        self.comment = Comment.objects.create(
            owner=self.user2,
            issue=self.issue,
            comment_area='Test Comment'
        )

    def test_like_comment(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(f'/api/comments/{self.comment.id}/likes/')

    def test_dislike_comment(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(f'/api/comments/{self.comment.id}/dislikes/')

    def test_like_duplicate_comment(self):
        # Create a like for the comment
        Like.objects.create(owner=self.user1, comment=self.comment)
        
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(f'/api/comments/{self.comment.id}/likes/')
        
        # Check the response status code and the number of likes in the database
        self.assertEqual(Like.objects.count(), 1)

    def test_dislike_duplicate_comment(self):
        # Create a dislike for the comment
        DisLike.objects.create(owner=self.user1, comment=self.comment)
        
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(f'/api/comments/{self.comment.id}/dislikes/')
        self.assertEqual(DisLike.objects.count(), 1)


