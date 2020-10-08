import unittest

from flask import Flask, json
from flask_sqlalchemy import SQLAlchemy
from models import setup_db


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = Flask(__name__)
        self.app.config.from_object('config')
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = f'postgres://postgres:root@localhost:5432/{self.database_name}'
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

    # result = self.client().get('/', json={'page': 1})
    # data = json.loads(result.data)
    def test_get_questions(self):
        result = self.client().get('/questions?page=2')
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])

    def test_create_question(self):
        result = self.client().post('/questions', json={
            'question': 'what is the best source of a very good quality courses',
            'answer': 'udacity',
            'category': 'any',
            'difficulty': 1
        })
        data = result.data

        self.assertEqual(result.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_search_question(self):
        result = self.client().post('questions/search', json={
            'search_term': 'what is'
        })
        data = result.data

        self.assertEqual(result.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_category'], 'any')

    def test_delete_question(self):
        result = self.client().delete('/questions/1')
        data = result.data

        self.assertEqual(result.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_categories(self):
        result = self.client().get('/categories')
        data = result.data

        self.assertEqual(result.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    def test_get_questions_by_category(self):
        result = self.client().get('/categories/1/questions')
        data = result.data

        self.assertEqual(result.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])

    def test_post_quizzes(self):
        result = self.client().get('/categories')
        data = result.data

        self.assertEqual(result.status_code, 200)
        self.assertEqual(data['success'], True)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
