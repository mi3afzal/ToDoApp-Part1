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

    def test_index_load(self):
        response = self.app.get('/', content_type='html/text')
        self.assertIn(b'To Do App Interface', response.data)

    def create_task(self, desc):
        response = self.app.post('/todo/api/v1.0/tasks', content_type='application/json',
                                 data=json.dumps({"title": "Unit Test", "description": "Test Desc from: "+desc}))
        return json.loads(response.get_data(as_text=True))

    def delete_task(self, task_id):
        response = self.app.delete('/todo/api/v1.0/tasks/'+task_id, content_type='application/json')
        json_response = json.loads(response.get_data(as_text=True))
        return json_response['response']

    def test_create_tasks(self):
        json_response = self.create_task('create')
        task_id = json_response['id']
        self.assertIsNotNone(task_id)

        json_response = self.delete_task(task_id)
        self.assertEqual(json_response['status'], 'success')

    def test_get_all_tasks(self):
        json_response = self.create_task('get all')
        task_id = json_response['id']
        self.assertIsNotNone(task_id)

        response = self.app.get('/todo/api/v1.0/tasks', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Unit Test', response.data)

        json_response = self.delete_task(task_id)
        self.assertEqual(json_response['status'], 'success')

    def test_get_task(self):
        # create a task first
        json_response = self.create_task('get')
        task_id = json_response['id']
        self.assertIsNotNone(task_id)

        response = self.app.get('/todo/api/v1.0/tasks/'+task_id, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Unit Test', response.data)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['tasks'][0]['done'], False)

        json_response = self.delete_task(task_id)
        self.assertEqual(json_response['status'], 'success')


if __name__ == '__main__':
    unittest.main()