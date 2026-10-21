import unittest
from app import app
class AppTests(unittest.TestCase):
    def setUp(self): self.client = app.test_client()
    def test_home_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Student Task Tracker", response.data)
    def test_health_endpoint(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "ok")
if __name__ == "__main__": unittest.main()
