#!/usr/bin/python3

import unittest
from unittest.mock import patch, Mock
from hbnb.app import create_app
import json

class TestUserEndpoints(unittest.TestCase):
    """Test cases for User API endpoints"""

    def setUp(self):
        """Set up test client and mocked dependencies"""
        self.app = create_app()
        self.client = self.app.test_client()
        self.test_user_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        }

    @patch('hbnb.app.services.facade.get_user_by_email')
    @patch('hbnb.app.services.facade.create_user')
    def test_create_user_success(self, mock_create_user, mock_get_user_by_email):
        """Test successful user creation"""
        # Mock user doesn't exist
        mock_get_user_by_email.return_value = None

        # Mock created user
        mock_user = Mock()
        mock_user.id = "test-uuid"
        mock_user.first_name = self.test_user_data["first_name"]
        mock_user.last_name = self.test_user_data["last_name"]
        mock_user.email = self.test_user_data["email"]
        mock_create_user.return_value = mock_user

        response = self.client.post(
            '/api/v1/users/',
            data=json.dumps(self.test_user_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data["first_name"], self.test_user_data["first_name"])
        self.assertEqual(data["last_name"], self.test_user_data["last_name"])
        self.assertEqual(data["email"], self.test_user_data["email"])
        self.assertTrue("id" in data)

    @patch('hbnb.app.services.facade.get_user_by_email')
    def test_create_user_duplicate_email(self, mock_get_user_by_email):
        """Test user creation with duplicate email"""
        # Mock user already exists
        mock_get_user_by_email.return_value = Mock()

        response = self.client.post(
            '/api/v1/users/',
            data=json.dumps(self.test_user_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data["error"], "Email already registered")

    def test_create_user_invalid_data(self):
        """Test user creation with invalid data"""
        invalid_data = {
            "first_name": "",
            "last_name": "Doe",
            "email": "invalid-email"
        }
        response = self.client.post(
            '/api/v1/users/',
            data=json.dumps(invalid_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 500)

    @patch('hbnb.app.services.facade.get_user')
    def test_get_user_success(self, mock_get_user):
        """Test successful user retrieval"""
        # Mock user
        mock_user = Mock()
        mock_user.id = "test-uuid"
        mock_user.first_name = self.test_user_data["first_name"]
        mock_user.last_name = self.test_user_data["last_name"]
        mock_user.email = self.test_user_data["email"]
        mock_get_user.return_value = mock_user

        response = self.client.get('/api/v1/users/test-uuid')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["first_name"], self.test_user_data["first_name"])
        self.assertEqual(data["last_name"], self.test_user_data["last_name"])
        self.assertEqual(data["email"], self.test_user_data["email"])

    @patch('hbnb.app.services.facade.get_user')
    def test_get_user_not_found(self, mock_get_user):
        """Test user retrieval when user doesn't exist"""
        mock_get_user.return_value = None

        response = self.client.get('/api/v1/users/non-existent-uuid')

        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data["error"], "User not found")

    @patch('hbnb.app.services.facade.get_user')
    def test_update_user_success(self, mock_get_user):
        """Test successful user update"""
        # Mock existing user
        mock_user = Mock()
        mock_user.id = "test-uuid"
        mock_user.update = Mock()
        mock_get_user.return_value = mock_user

        update_data = {
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane.smith@example.com"
        }

        response = self.client.put(
            '/api/v1/users/test-uuid',
            data=json.dumps(update_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        mock_user.update.assert_called_once_with(update_data)

    @patch('hbnb.app.services.facade.get_user')
    def test_update_user_not_found(self, mock_get_user):
        """Test user update when user doesn't exist"""
        mock_get_user.return_value = None

        update_data = {
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane.smith@example.com"
        }

        response = self.client.put(
            '/api/v1/users/non-existent-uuid',
            data=json.dumps(update_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data["error"], "User not found")


if __name__ == '__main__':
    unittest.main()