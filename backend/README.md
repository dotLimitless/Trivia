# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
python app.py
```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

## API Reference
### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as proxy in the frontend configuration.
- Authentication: This version of the application does not require authentication or API keys.
### Error Handling
Errors are returned as JSON objects in the following format:
```json
{
    "success": false,
    "error": 520,
    "reason": "Duplicate entry 'foobar' for key 'question'",
    "message": "An error occurred, question could not be stored"
}
```
The API will return one error type when requests fail:
- 520 Unknown error
- 400 Bad request
- 404 Not found
### Endpoints
#### GET /questions
- General:
    - Returns a list of question objects, total number of questions, a list of category objects, and a success value.
    - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
- Sample `curl http://127.0.0.1:5000/questions?page=2`
```json
{
    "success": true,
    "questions": [{
        "id": 11,
        "question": "what is the gravity of earth",
        "answer": "9.807 m/s²",
        "category": "physics",
        "difficulty": 1
    },
    {
        "id": 12,
        "question": "what is the gravity of earth",
        "answer": "9.807 m/s²",
        "category": "physics",
        "difficulty": 1
    },
    {
        "id": 13,
        "question": "what is the gravity of earth",
        "answer": "9.807 m/s²",
        "category": "physics",
        "difficulty": 1
    },
    {
        "id": 14,
        "question": "what is the gravity of earth",
        "answer": "9.807 m/s²",
        "category": "physics",
        "difficulty": 1
    },
    {
        "id": 15,
        "question": "what is the gravity of earth",
        "answer": "9.807 m/s²",
        "category": "physics",
        "difficulty": 1
    },
    {
        "id": 16,
        "question": "what is the gravity of earth",
        "answer": "9.807 m/s²",
        "category": "physics",
        "difficulty": 1
    },
    {
        "id": 17,
        "question": "what is the gravity of earth",
        "answer": "9.807 m/s²",
        "category": "physics",
        "difficulty": 1
    },
    {
        "id": 18,
        "question": "what is the gravity of earth",
        "answer": "9.807 m/s²",
        "category": "physics",
        "difficulty": 1
    },
    {
        "id": 19,
        "question": "what is the gravity of earth",
        "answer": "9.807 m/s²",
        "category": "physics",
        "difficulty": 1
    },
    {
        "id": 20,
        "question": "what is the gravity of earth",
        "answer": "9.807 m/s²",
        "category": "physics",
        "difficulty": 1
    }],
    "total_questions": 30,
    "categories": [{
        "id": 1,
        "type": "any"
    },
    {
        "id": 2,
        "type": "Art"
    }],
    "current_category": "any"
}
```
#### POST /questions
- General:
    - Creates a new question using the submitted question, answer, category(optional), difficulty. Returns a success value.
- Sample `curl http://127.0.0.1:5000/questions`
```json
{
    "success": true
}
```
#### POST /questions/search
- General:
    - Returns a list of question objects that contains the submitted search term, total number of questions, current category, and a success value.
- Sample `curl http://127.0.0.1:5000/questions/search`
```json
{
    "success": true,
    "questions": [
        {
            "question": "what is the best source of a very good quality courses",
            "answer":  "udacity",
            "category": "any",
            "difficulty": 1
        },
        {
            "question": "what is the gravity of earth",
            "answer":  "at udacity",
            "category": "any",
            "difficulty": 1
        }],
    "total_questions": 30,
    "current_category": "any"
}
```
#### DELETE /questions/\<int:question_id>
- General:
    - Delete a question with the give id.
    - Returns a success value.
- Sample `curl http://127.0.0.1:5000/questions/1`
```json
{
    "success": true
}
```
#### GET /categories
- General:
    - Returns a list of category objects, success value.
- Sample `curl http://127.0.0.1:5000/categories`
```json
{
    "success": true,
    "categories":  [{
        "id": 1,
        "type": "Art"
    },
    {
        "id": 2,
        "type": "Science"
    },
    {
        "id": 3,
        "type": "Entertainment"
    }]
}
```
#### GET /categories/\<int:category_id>/questions
- General:
    - Returns a success value, list of question objects that are in the specified category id, total questions, current category.
- Sample `curl http://127.0.0.1:5000/categories/\<int:category_id>/questions`
```json
{
    "success": true,
    "questions": [{
            "question": "what is the best source of a very good quality courses",
            "answer":  "udacity",
            "category": "any",
            "difficulty": 1
        },
        {
            "question": "what is the gravity of earth",
            "answer":  "at udacity",
            "category": "any",
            "difficulty": 1
        }],
    "total_questions": 30,
    "current_category": "Art"
}
```
#### POST /quizzes
```json
{
    "success": true,
    "question": {
        "question": "what is the best source of a very good quality courses",
        "answer":  "udacity",
        "category": "any",
        "difficulty": 1
    }
}
```
## Author
dotLimitless <3