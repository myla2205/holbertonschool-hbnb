#!/usr/bin/python3

import unittest
from unittest.mock import patch
from hbnb.app import create_app
from hbnb.app.models.user import User
from hbnb.app.models.place import Place
from hbnb.app.models.review import Review
from uuid import uuid4

class TestReviewEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

        # Create mock user and place for testing
        self.user = User(first_name="John", last_name="Doe", email="john@example.com")
        self.user.id = str(uuid4())

        self.place = Place(title="Test Place", description="Test Description", price=100, latitude=50, longitude=50, owner=self.user)
        self.place.id = str(uuid4())

        # Sample valid review data
        self.valid_review_data = {
            "text": "Great place!",
            "rating": 5,
            "user_id": self.user.id,
            "place_id": self.place.id
        }

    def test_create_review_success(self):
        """Test successful review creation"""
        with patch('app.services.facade.create_review') as mock_create:
            # Create a mock review object
            mock_review = Review(
                text=self.valid_review_data["text"],
                rating=self.valid_review_data["rating"],
                user=self.user,
                place=self.place
            )
            mock_review.id = str(uuid4())
            mock_create.return_value = mock_review

            response = self.client.post('/api/v1/reviews/', json=self.valid_review_data)

            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.json['text'], "Great place!")
            self.assertEqual(response.json['rating'], 5)
            self.assertEqual(response.json['user_id'], self.user.id)
            self.assertEqual(response.json['place_id'], self.place.id)

    def test_create_review_invalid_rating(self):
        """Test review creation with invalid rating"""
        invalid_data = self.valid_review_data.copy()
        invalid_data['rating'] = 6  # Rating should be 1-5

        response = self.client.post('/api/v1/reviews/', json=invalid_data)

        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)

    def test_create_review_empty_text(self):
        """Test review creation with empty text"""
        invalid_data = self.valid_review_data.copy()
        invalid_data['text'] = ""

        response = self.client.post('/api/v1/reviews/', json=invalid_data)

        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)

    def test_get_all_reviews(self):
        """Test retrieving all reviews"""
        with patch('hbnb.app.services.facade.get_all_reviews') as mock_get_all:
            mock_review = Review(
                text="Test review",
                rating=4,
                user=self.user,
                place=self.place
            )
            mock_review.id = str(uuid4())
            mock_get_all.return_value = [mock_review]

            response = self.client.get('/api/v1/reviews/')

            self.assertEqual(response.status_code, 200)
            self.assertTrue(isinstance(response.json, list))
            self.assertEqual(len(response.json), 1)
            self.assertEqual(response.json[0]['text'], "Test review")

    def test_get_review_by_id(self):
        """Test retrieving a specific review by ID"""
        review_id = str(uuid4())
        with patch('hbnb.app.services.facade.get_review') as mock_get:
            mock_review = Review(
                text="Test review",
                rating=4,
                user=self.user,
                place=self.place
            )
            mock_review.id = review_id
            mock_get.return_value = mock_review

            response = self.client.get(f'/api/v1/reviews/{review_id}')

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['id'], review_id)
            self.assertEqual(response.json['text'], "Test review")

    def test_get_nonexistent_review(self):
        """Test retrieving a review that doesn't exist"""
        with patch('hbnb.app.services.facade.get_review') as mock_get:
            mock_get.return_value = None

            response = self.client.get(f'/api/v1/reviews/{str(uuid4())}')

            self.assertEqual(response.status_code, 404)
            self.assertIn('error', response.json)

    def test_update_review(self):
        """Test updating a review"""
        review_id = str(uuid4())
        update_data = {
            "text": "Updated review",
            "rating": 3,
            "user_id": self.user.id,
            "place_id": self.place.id
        }

        with patch('hbnb.app.services.facade.get_review') as mock_get:
            with patch('hbnb.app.services.facade.update_review') as mock_update:
                mock_review = Review(
                    text=update_data["text"],
                    rating=update_data["rating"],
                    user=self.user,
                    place=self.place
                )
                mock_review.id = review_id
                mock_get.return_value = mock_review
                mock_update.return_value = mock_review

                response = self.client.put(f'/api/v1/reviews/{review_id}', json=update_data)

                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json['text'], "Updated review")
                self.assertEqual(response.json['rating'], 3)

    def test_delete_review(self):
        """Test deleting a review"""
        review_id = str(uuid4())
        with patch('hbnb.app.services.facade.get_review') as mock_get:
            with patch('hbnb.app.services.facade.delete_review') as mock_delete:
                mock_review = Review(
                    text="Test review",
                    rating=4,
                    user=self.user,
                    place=self.place
                )
                mock_review.id = review_id
                mock_get.return_value = mock_review

                response = self.client.delete(f'/api/v1/reviews/{review_id}')

                self.assertEqual(response.status_code, 200)
                self.assertIn('message', response.json)
                mock_delete.assert_called_once_with(review_id)

    def test_get_reviews_by_place(self):
        """Test retrieving all reviews for a specific place"""
        place_id = str(uuid4())
        with patch('hbnb.app.services.facade.get_reviews_by_place') as mock_get_by_place:
            mock_review = Review(
                text="Place review",
                rating=5,
                user=self.user,
                place=self.place
            )
            mock_review.id = str(uuid4())
            mock_get_by_place.return_value = [mock_review]

            response = self.client.get(f'/api/v1/reviews/places/{place_id}/reviews')

            self.assertEqual(response.status_code, 200)
            self.assertTrue(isinstance(response.json, list))
            self.assertEqual(len(response.json), 1)
            self.assertEqual(response.json[0]['text'], "Place review")

    def test_get_reviews_nonexistent_place(self):
        """Test retrieving reviews for a place that doesn't exist"""
        with patch('hbnb.app.services.facade.get_reviews_by_place') as mock_get_by_place:
            mock_get_by_place.return_value = None

            response = self.client.get(f'/api/v1/reviews/places/{str(uuid4())}/reviews')

            self.assertEqual(response.status_code, 404)
            self.assertIn('error', response.json)

if __name__ == '__main__':
    unittest.main()