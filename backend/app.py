from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_restful import abort
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
    page = int(request.args['page'])

    if page > max_page:
        abort(404)

    start = page * questions_per_page - questions_per_page
    question_list = [question.format() for question in Question.query.offset(start).limit(questions_per_page).all()]
    category_list = get_categories()

    return jsonify({
        'success': True,
        'questions': question_list,
        'total_questions': total_questions,
        'categories': category_list,
        'current_category': ''
    })


@app.route('/questions', methods=["POST"])
def store_question():
    """
        store a question to the database
    """
    global total_questions
    data = request.get_json()
    category = data.get('category')

    if not Category.query.filter(Category.id == int(category)).first():
        abort(400)

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
        abort(500)
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
    questions_list = Question.query.filter(func.lower(Question.question).contains(func.lower(data['searchTerm']))).all()
    result = [question.format() for question in questions_list]

    category = ''

    if result[0]:
        category = result[0]['category']

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
        abort(500)
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

    return jsonify({
        'success': True,
        'categories': get_categories()
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
             Question.query.filter(Question.category == str(category.id)).all()]
    current_category = category.type

    return jsonify({
        'success': True,
        'questions': value,
        'total_questions': total_questions,
        'current_category': current_category
    })


@app.route('/quizzes', methods=["POST"])
def quizze():
    """
        returns a random question with the specified category, excluding the current question
    """
    data = request.get_json()
    prev_questions = data['previous_questions']

    question = Question.query.filter(Question.category == str(data['quiz_category']['id'])) \
        .filter(~Question.id.in_(prev_questions)).order_by(func.random()).first()

    return jsonify({
        'success': True,
        'question': question.format() if question else None
    })


def get_categories():
    return [category.format() for category in Category.query.all()]


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Not Found"
    }), 404


@app.errorhandler(500)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "Internal Server Error"
    }), 500


@app.errorhandler(400)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Bad Request"
    }), 400


if __name__ == '__main__':
    app.run()
