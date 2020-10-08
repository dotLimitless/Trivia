import math

from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError

from models import db, setup_db, Question, Category

app = Flask(__name__)
app.config.from_object('config')
setup_db(app)
questions_per_page = 10
total_questions = Question.query.count()
max_page = total_questions / 10
CORS(app)


@app.route('/questions')
def questions():
    """
        returns a list of questions from the database
        starting from the (page * questions_per_page(default 10) - questions_per_page(default 10))
        ending after questions_per_page limit is reached
    """
    page = request.args['page']

    if page > max_page:
        return jsonify({
            'success': False,
            'status': 404,
            'reason': f'the submitted page number {page} is greater than the maximum number of pages {max_page}',
            'message': 'resource not found'
        })

    start = page * questions_per_page - questions_per_page
    question_list = [question.format() for question in Question.query.offset(start).limit(questions_per_page).all()]
    category_list = []

    for question in question_list:
        category_list.append(Category.query.filter(Category.type == question.category).first())

    current_category = ''

    if category_list[0]:
        current_category = category_list[0].type

    return jsonify({
        'success': True,
        'questions': question_list,
        'total_questions': total_questions,
        'categories': category_list,
        'current_category': current_category
    })


@app.route('/questions', methods=["POST"])
def store_question():
    """
        store a question to the database
    """
    global total_questions
    data = request.get_json()
    category = data.get('category', 'any')

    if not Category.query.filter(Category.type == category).first():
        return jsonify({
            'success': False,
            'error': 400,
            'reason': f'Category {category} was not found',
            'message': 'An error occurred, question could not be stored'
        })

    question = Question(
        question=data['question'],
        answer=data['answer'],
        category=category,
        difficulty=data['difficulty'])

    try:
        question.insert()
        total_questions += 1
    except SQLAlchemyError as e:
        db.session.rollback()

        return jsonify({
            'success': False,
            'error': 520,
            'reason': e.args,
            'message': 'An error occurred, question could not be stored'
        })
    finally:
        db.session.close()

    return jsonify({
        'success': True
    })


@app.route('/questions/search', methods=["POST"])
def search_question():
    """
        returns all questions that contains the given word
    """
    data = request.get_json()
    result = [question.format() for question in
              Question.query.filter(
                  func.lower(Question.question).contains(func.lower(data['searchTerm']))).all()]

    category = ''

    if result[0]:
        category = result[0].category

    return jsonify({
        'success': True,
        'questions': result,
        'total_questions': total_questions,
        'current_category': category
    })


@app.route('/questions/<int:question_id>', methods=["DELETE"])
def delete_question(question_id: int):
    """
        delete a question with the specified id
    """
    global total_questions
    question = Question.query.get(question_id)

    try:
        question.delete()
        total_questions -= 1
    except SQLAlchemyError as e:
        db.session.rollback()

        return jsonify({
            'success': False,
            'error': 520,
            'reason': e.args,
            'message': 'An error occurred, question could not be deleted'
        })
    finally:
        db.session.close()

    return jsonify({
        'success': True
    })


@app.route('/categories')
def categories():
    """
        returns all categories in the database
    """
    result = [category.format() for category in Category.query.all()]

    return jsonify({
        'success': True,
        'categories': result
    })


@app.route('/categories/<int:category_id>/questions')
def questions_by_category(category_id: int):
    """
        returns
        - all questions with the specified category
        - number of total questions with the specified category
        - current category type
    """
    category = Category.query.get(category_id)
    value = [question.format() for question in
             Question.query.filter(Question.category == category.type).all()]

    current_category = ''

    if category:
        current_category = category.type

    return jsonify({
        'success': True,
        'questions': value,
        'total_questions': total_questions,
        'current_category ': current_category
    })


@app.route('/quizzes', methods=["POST"])
def quizze():
    """
        returns a random question with the specified category, excluding the current question
    """
    data = request.get_json()
    prev_questions = data['previous_questions']
    category = data['quiz_category']
    question = Question.query.filter(Question.category == category) \
        .filter(Question.question != prev_questions).order_by(func.random()).first()

    return jsonify({
        'success': True,
        'question': question
    })


if __name__ == '__main__':
    app.run()
