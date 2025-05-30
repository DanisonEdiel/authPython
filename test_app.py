import unittest
from app import app


class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_hello_route(self):
        response = self.app.get('/api/hello')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('message', data)
        self.assertIn('suma', data)
        self.assertEqual(data['resultado'], 8)

    def test_index_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('message', data)


if __name__ == '__main__':
    unittest.main()
