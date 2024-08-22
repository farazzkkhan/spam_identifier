from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

class UserAuthTests(APITestCase):

    def setUp(self):
        self.signup_url = '/api/signup/'
        self.login_url = '/api/login/'
        self.user_data = {
            'username': 'testuser',
            'password': 'testpassword',
            'phone_number': '1234567890'
        }

    def test_signup(self):
        response = self.client.post(self.signup_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], self.user_data['username'])
        self.assertTrue('password' not in response.data)  # Password should not be returned in response

    def test_login(self):
        self.client.post(self.signup_url, self.user_data, format='json')
        response = self.client.post(self.login_url, {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_login_invalid_credentials(self):
        response = self.client.post(self.login_url, {
            'username': self.user_data['username'],
            'password': 'wrongpassword'
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Invalid credentials')
