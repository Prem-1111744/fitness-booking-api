import unittest
import json
from app import app, init_db, seed_classes

class FitnessBookingTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        with app.app_context():
            init_db()
            seed_classes()

    def test_get_classes(self):
        response = self.app.get('/classes')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)
        self.assertIn('name', data[0])

    def test_booking_and_get_bookings(self):
        # Book a class
        response = self.app.post('/book', json={
            "class_id": 1,
            "client_name": "Test User",
            "client_email": "test@example.com"
        })
        self.assertEqual(response.status_code, 200)
        booking = json.loads(response.data)
        self.assertEqual(booking['client_email'], "test@example.com")

        # Get bookings by email
        response2 = self.app.get('/bookings?email=test@example.com')
        self.assertEqual(response2.status_code, 200)
        bookings = json.loads(response2.data)
        self.assertEqual(len(bookings), 1)
        self.assertEqual(bookings[0]['client_email'], "test@example.com")

    def test_booking_missing_fields(self):
        response = self.app.post('/book', json={})
        self.assertEqual(response.status_code, 400)
        error = json.loads(response.data)
        self.assertIn("error", error)

if __name__ == '__main__':
    unittest.main()