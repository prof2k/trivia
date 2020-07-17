import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = f"postgresql://postgres:password@localhost:5432/{self.database_name}"
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = res.json

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))

    def test_get_questions(self):
        res = self.client().get('/questions')
        data = res.json

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertLessEqual(len(data['questions']), 10)

    def test_404_get_question(self):
        res = self.client().get('/questions?page=1000')
        data = res.json

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_delete_question(self):
        res = self.client().delete('/questions/13')
        data = res.json

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_delete_question(self):
        res = self.client().delete('/questions/1000')
        data = res.json

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_add_question(self):
        body = {
            'question': "Some incredibly fun question",
            'answer': 'Fabulous Of Course',
            'category': 2,
            'difficulty': 5
        }

        res = self.client().post('/questions', data=json.dumps(body), content_type='application/json')
        data = res.json

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_400_add_question(self):
        body = {
            'question': 22039,
            'answer': 22,
            'category': "Tech",
            'difficulty': "Hello"
        }

        res = self.client().post('/questions', data=json.dumps(body), content_type='application/json')
        data  = res.json

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_search_query(self):
        res = self.client().get('/questions?q=title')
        data = res.json

        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertLessEqual(len(data['questions']), 10)

    def test_404_search_query(self):
        res = self.client().get('/questions?q=Icantbefound')
        data = res.json

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_questions_by_category(self):
        res = self.client().get('/questions?cat=3')
        data = res.json

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['questions']))
        self.assertLessEqual(len(data['questions']), 10)

    def test_404_questions_by_category(self):
        res = self.client().get('/questions?cat=1000')
        data = res.json

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()