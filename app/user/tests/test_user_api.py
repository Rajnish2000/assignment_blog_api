"""
 Test user API.
"""
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from django.test import TestCase
from django.contrib.auth import get_user_model


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:login')
PROFILE_URL = reverse('user:profile')


def create_user(**params):
    """ Create and return a new user """
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """ Class for public user API tests """

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """ Test creating a user is successful """
        payload = {
            'username': 'testuser',
            'email': 'test1@example.com',
            'password': 'testexample123',
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists_error(self):
        """ Test error returned if user with email exists """
        payload = {
            'username': 'testuser',
            'email': 'test1@example.com',
            'password': 'testexample123',
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """ Test error returned if password is too short """
        payload = {
            'username': 'testuser',
            'email': 'test1@example.com',
            'password': 'tes',
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_on_user_login(self):
        """Test generating token for valid credentials"""
        user_details = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword123'
        }
        payload = {
            'username': user_details['email'],
            'password': user_details['password'],
        }
        create_user(**user_details)
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_login_and_token_check_for_invalid_credentials(self):
        """ Test invalid credentials """
        create_user(username='testuser',
                    email='test@example.com',
                    password='test123')
        payload = {
            'email': 'test2@example.com',
            'password': 'test123',
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)

    def test_token_for_blank_password(self):
        """ Test token for blank password """
        payload = {'email': 'test@example.com', 'password': ''}
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """ Test authentication is required for users """
        res = self.client.get(PROFILE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """ Test API requests that require authentication """

    def setUp(self):
        self.user = create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """ Test retrieving profile for logged in user """
        res = self.client.get(PROFILE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'username': self.user.username,
            'email': self.user.email,
        })

    def test_post_profile_not_allowed(self):
        """ Test POST is not allowed on the profile url """
        res = self.client.post(PROFILE_URL, {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """ Test updating the user profile for authenticated user """
        payload = {'username': 'newusername', 'password': 'newpassword123'}
        res = self.client.patch(PROFILE_URL, payload)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, payload['username'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
