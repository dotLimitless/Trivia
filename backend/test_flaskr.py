import json
import unittest

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import setup_db, db, Question, Category
from app import app


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.app.config['DEBUG'] = False
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = f'postgres://postgres:root@localhost:5432/{self.database_name}'
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = db

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_questions(self):
        result = self.client().get('/questions?page=1')
        self.assertEqual(result.status_code, 200)
        data = json.loads(result.data)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['questions'])
        self.assertIsNotNone(data['total_questions'])
        self.assertIsNotNone(data['current_category'])

    def test_get_questions_fail(self):
        result = self.client().get('/questions?page=999')
        self.assertEqual(result.status_code, 404)
        data = json.loads(result.data)
        self.assertEqual(data['success'], False)

    def test_create_question(self):
        result = self.client().post('/questions', json={
            'question': 'what is the best source of a very good quality courses',
            'answer': 'udacity',
            'category': '1',
            'difficulty': 1
        })
        self.assertEqual(result.status_code, 200)
        data = json.loads(result.data)
        self.assertEqual(data['success'], True)

    def test_create_question_fail(self):
        result = self.client().post('/questions', json={
            'question': 'what is the best source of a very good quality courses',
            'answer': 'udacity',
            'category': '999',
            'difficulty': 1
        })
        self.assertEqual(result.status_code, 400)
        data = json.loads(result.data)
        self.assertEqual(data['success'], False)

    def test_search_questions(self):
        result = self.client().post('questions/search', json={
            'searchTerm': 'what'
        })
        self.assertEqual(result.status_code, 200)
        data = json.loads(result.data)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['questions'])
        self.assertIsNotNone(data['total_questions'])
        self.assertIsNotNone(data['current_category'])

    def test_search_questions_fail(self):
        result = self.client().post('questions/search', json={
            'searchTerm': '999'
        })
        self.assertEqual(result.status_code, 404)
        data = json.loads(result.data)
        self.assertEqual(data['success'], False)

    def test_delete_question(self):
        question = Question.query.first()
        result = self.client().delete(f'/questions/{question.id}')
        self.assertEqual(result.status_code, 200)
        data = json.loads(result.data)
        self.assertEqual(data['success'], True)

    def test_delete_question_fail(self):
        result = self.client().delete(f'/questions/9999')
        self.assertEqual(result.status_code, 500)
        data = json.loads(result.data)
        self.assertEqual(data['success'], False)

    def test_get_categories(self):
        result = self.client().get('/categories')
        self.assertEqual(result.status_code, 200)
        data = json.loads(result.data)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['categories'])

    def test_get_questions_by_category(self):
        result = self.client().get('/categories/1/questions')
        self.assertEqual(result.status_code, 200)
        data = json.loads(result.data)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['questions'])
        self.assertIsNotNone(data['total_questions'])
        self.assertIsNotNone(data['current_category'])

    def test_get_questions_by_category_fail(self):
        result = self.client().get('/categories/999/questions')
        self.assertEqual(result.status_code, 404)
        data = json.loads(result.data)
        self.assertEqual(data['success'], False)

    def test_post_quizzes(self):
        question = Question.query.first()
        result = self.client().post('/quizzes', json={
            'previous_questions': [question.id],
            'quiz_category': {
                'id': question.category,
            }
        })
        self.assertEqual(result.status_code, 200)
        data = json.loads(result.data)
        self.assertEqual(data['success'], True)

    def test_post_quizzes_fail(self):
        result = self.client().post('/quizzes', json={
            'previous_questions': [999],
            'quiz_category': {
                'id': 999,
                'type': 'Fake'
            }
        })
        self.assertEqual(result.status_code, 404)
        data = json.loads(result.data)
        self.assertEqual(data['success'], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
