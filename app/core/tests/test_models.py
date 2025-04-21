"""
 Test for the models.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email(self):
        username = "testuser"
        email = "test@example.com"
        password = "testpassword123"
        user = get_user_model().objects.create_user(
            username=username,
            email=email,
            password=password
        )
        self.assertEqual(user.username, username)
        self.assertEqual(user.email, email)
        self.assertEqual(user.check_password(password), True)

    def test_new_user_email_normalized(self):
        '''Test the email is normalized for new users.'''
        sample_emails = [
            ['user1', 'test1@example.com', 'test1@example.com'],
            ['user2', 'Test2@example.com', 'Test2@example.com'],
            ['user3', 'TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['user4', 'test4@example.COM', 'test4@example.com'],
        ]
        for username, email, expected in sample_emails:
            user = get_user_model().objects.create_user(
                username=username, email=email, password='test123'
            )
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        '''Test that creating a user without an email raises a ValueError.'''
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                username='user123', email='', password='test123'
            )

    def test_create_superuser(self):
        '''Test for creating a superuser.'''
        user = get_user_model().objects.create_superuser(
            'testuser',
            'test@example.com',
            'test123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_blog_model(self):
        """Test for creating a blog post model is successful."""
        user = get_user_model().objects.create_user(
            'testuser',
            'test@example.com',
            'test123'
        )
        blog_post = models.BlogPost.objects.create(
            title='Test Blog Post',
            content='This is a test blog post.',
            author=user
        )
        self.assertEqual(str(blog_post), blog_post.title)
