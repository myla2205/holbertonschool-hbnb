#!/usr/bin/python3

import unittest
from unittest.mock import patch, Mock
import json
from hbnb.app import create_app

class TestPlaceEndpoints(unittest.TestCase):
    def setUp(self):
        """Set up test client and mocked data"""
        self.app = create_app()
        self.client = self.app.test_client()

        # Mock place data
        self.test_place_data = {
            "id": "test-place-uuid",
            "name": "Test Place",
            "user_id": "test-user-uuid",
            "city_id": "test_city_id",
            "description": "Test description",
            "amenities": []
        }

    def create_mock_place(self):
        """Helper method to create a properly configured mock place"""
        class MockPlace:
            def __init__(self, data):
                self.id = data["id"]
                self.name = data["name"]
                self.user_id = data["user_id"]
                self.city_id = data["city_id"]
                self.description = data["description"]
                self.amenities = []

            def to_dict(self):
                return {
                    "id": self.id,
                    "name": self.name,
                    "user_id": self.user_id,
                    "city_id": self.city_id,
                    "description": self.description,
                    "amenities": self.amenities
                }

            def update(self, data):
                for key, value in data.items():
                    setattr(self, key, value)

        return MockPlace(self.test_place_data)


    @patch('hbnb.app.services.facade.get_place')
    def test_update_place(self, mock_get_place):
        """Test updating a place"""
        mock_place = self.create_mock_place()
        mock_get_place.return_value = mock_place

        update_data = {"name": "Updated Place"}

        response = self.client.put(
            f'/api/v1/places/{self.test_place_data["id"]}',
            data=json.dumps(update_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)

    @patch('hbnb.app.services.facade.get_place')
    def test_get_place_not_found(self, mock_get_place):
        """Test getting a non-existent place"""
        mock_get_place.return_value = None

        response = self.client.get('/api/v1/places/non-existent-id')

        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data.get("error"), "Place not found")

    @patch('hbnb.app.services.facade.get_place')
    def test_update_place_not_found(self, mock_get_place):
        """Test updating a non-existent place"""
        mock_get_place.return_value = None

        update_data = {"name": "Updated Place"}
        response = self.client.put(
            '/api/v1/places/non-existent-id',
            data=json.dumps(update_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data.get("error"), "Place not found")


if __name__ == '__main__':
    unittest.main()