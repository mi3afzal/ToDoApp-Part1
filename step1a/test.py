from app import app
import unittest
import json

class AppTestCase(unittest.TestCase):
    def setUp(self):
        print("Setting Up ")
        app.config['TESTING'] = True
        self.app = app.test_client()


    def tearDown(self):
        print("Tearing down ")


    def test_index(self):
        response = self.app.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hello World', response.data)



if __name__ == '__main__':
    unittest.main()