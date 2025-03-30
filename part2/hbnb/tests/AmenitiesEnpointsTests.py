#!/usr/bin/python3

import unittest
from unittest.mock import patch, Mock
from hbnb.app import create_app
import json

class TestAmenityEndpoints(unittest.TestCase):
    """Test cases for Amenity API endpoints"""

    def setUp(self):
        """Set up test client and mocked dependencies"""
        self.app = create_app()
        self.client = self.app.test_client()
        self.test_amenity_data = {
            "name": "Swimming Pool"
        }

    @patch('hbnb.app.services.facade.create_amenity')
    def test_create_amenity_success(self, mock_create_amenity):
        """Test successful amenity creation"""
        # Mock created amenity
        mock_amenity = Mock()
        mock_amenity.id = "test-uuid"
        mock_amenity.name = self.test_amenity_data["name"]
        mock_create_amenity.return_value = mock_amenity

        response = self.client.post(
            '/api/v1/amenities/',
            data=json.dumps(self.test_amenity_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data["name"], self.test_amenity_data["name"])
        self.assertTrue("id" in data)

    def test_create_amenity_missing_name(self):
        """Test amenity creation with missing name"""
        invalid_data = {}

        response = self.client.post(
            '/api/v1/amenities/',
            data=json.dumps(invalid_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data["error"], "Invalid input data")

    @patch('hbnb.app.services.facade.get_all_amenities')
    def test_get_all_amenities(self, mock_get_all_amenities):
        """Test retrieving all amenities"""
        # Mock list of amenities
        mock_amenity1 = Mock()
        mock_amenity1.id = "test-uuid-1"
        mock_amenity1.name = "Swimming Pool"

        mock_amenity2 = Mock()
        mock_amenity2.id = "test-uuid-2"
        mock_amenity2.name = "Gym"

        mock_get_all_amenities.return_value = [mock_amenity1, mock_amenity2]

        response = self.client.get('/api/v1/amenities/')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["name"], "Swimming Pool")
        self.assertEqual(data[1]["name"], "Gym")

    @patch('hbnb.app.services.facade.get_amenity')
    def test_get_amenity_success(self, mock_get_amenity):
        """Test successful amenity retrieval"""
        # Mock amenity
        mock_amenity = Mock()
        mock_amenity.id = "test-uuid"
        mock_amenity.name = self.test_amenity_data["name"]
        mock_get_amenity.return_value = mock_amenity

        response = self.client.get('/api/v1/amenities/test-uuid')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["name"], self.test_amenity_data["name"])
        self.assertEqual(data["id"], "test-uuid")

    @patch('hbnb.app.services.facade.get_amenity')
    def test_get_amenity_not_found(self, mock_get_amenity):
        """Test amenity retrieval when amenity doesn't exist"""
        mock_get_amenity.return_value = None

        response = self.client.get('/api/v1/amenities/non-existent-uuid')

        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data["error"], "Amenity not found")

    @patch('hbnb.app.services.facade.get_amenity')
    @patch('hbnb.app.services.facade.update_amenity')
    def test_update_amenity_success(self, mock_update_amenity, mock_get_amenity):
        """Test successful amenity update"""
        # Mock existing amenity
        mock_amenity = Mock()
        mock_amenity.id = "test-uuid"
        mock_get_amenity.return_value = mock_amenity

        # Mock updated amenity
        mock_updated = Mock()
        mock_updated.id = "test-uuid"
        mock_updated.name = "Updated Pool"
        mock_update_amenity.return_value = mock_updated

        update_data = {
            "name": "Updated Pool"
        }

        response = self.client.put(
            '/api/v1/amenities/test-uuid',
            data=json.dumps(update_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["amenity"]["name"], "Updated Pool")
        self.assertEqual(data["message"], "Amenity updated successfully")

    @patch('hbnb.app.services.facade.get_amenity')
    def test_update_amenity_not_found(self, mock_get_amenity):
        """Test amenity update when amenity doesn't exist"""
        mock_get_amenity.return_value = None

        update_data = {
            "name": "Updated Pool"
        }

        response = self.client.put(
            '/api/v1/amenities/non-existent-uuid',
            data=json.dumps(update_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data["error"], "Amenity not found")

    def test_update_amenity_missing_name(self):
        """Test amenity update with missing name"""
        invalid_data = {}

        response = self.client.put(
            '/api/v1/amenities/test-uuid',
            data=json.dumps(invalid_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data["error"], "Amenity name is required")


if __name__ == '__main__':
    unittest.main()