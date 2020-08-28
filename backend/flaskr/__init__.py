import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from sqlalchemy import func

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    '''
    
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    
    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-type, Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        return response
    
    '''
    @TODO: 
    Create an endpoint to handle GET requests 
    for all available categories.
    '''
    
    @app.route('/categories')
    def get_categories():
        categories = Category.query.all()
        categories_response = [category.format() for category in categories]
        return jsonify({
            'status_code': 200,
            'success': True,
            'data': categories_response,
        })

    '''
    @TODO: 
    Create an endpoint to handle GET requests for questions, 
    including pagination (every 10 questions). 
    This endpoint should return a list of questions, 
    number of total questions, current category, categories. 

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions. 
    '''
    @app.route('/questions')
    def get_questions():
        questions = Question.query.all()
        questions_formatted = [question.format() for question in questions]
        page = request.args.get('page', 1, type=int)
        
        if page < 0:
          abort(422)
        
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = page * QUESTIONS_PER_PAGE

        categories = Category.query.all()
        category_formatted = [category.format() for category in categories]

        return jsonify({
          'status_code': 200,
          'success': True,
          'questions': questions_formatted[start:end],
          'total_questions': len(questions_formatted),
          'current_category': None,
          'categories': category_formatted,
        })

    '''
    @TODO: 
    Create an endpoint to DELETE question using a question ID. 

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page. 
    '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.filter_by(id=question_id).one_or_none()
        if question is None:
            abort(404)

        question.delete()
        return jsonify({
          'status_code': 200,
          'success': True,
          'deleted': question_id,
          'message': 'The question was successfully deleted.'
        })

    '''
    @TODO: 
    Create an endpoint to POST a new question, 
    which will require the question and answer text, 
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab, 
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.  
    '''
    @app.route('/questions', methods=['POST'])
    def create_question():
        request_value = request.get_json()

        if request_value['question'] is None or request_value['answer'] is None:
            abort(422)
        
        if request_value['category'] is None or request_value['difficulty'] is None:
            abort(422)

        question = Question(
          request_value['question'], 
          request_value['answer'],
          request_value['category'],
          request_value['difficulty']
          )
        question.insert()
          
        return jsonify({
          'status_code': 200,
          'question': question.format(),
          'message': 'The question was successfully created',
          'success': True,
        })

    '''
    @TODO: 
    Create a POST endpoint to get questions based on a search term. 
    It should return any questions for whom the search term 
    is a substring of the question. 

    TEST: Search by any phrase. The questions list will update to include 
    only question that include that string within their question. 
    Try using the word "title" to start. 
    '''
    @app.route('/questions/searches', methods=['POST'])
    def search_question():
        search_term = request.get_json()['searchTerm']
        all_questions = Question.query.filter(Question.question.ilike('%{}%'.format(search_term))).all()
        questions = [question.format() for question in all_questions]

        return jsonify({
          'success': True,
          'questions': questions,
          'total_questions': len(questions),
          'current_category': None,
        })


    '''
    @TODO: 
    Create a GET endpoint to get questions based on category. 

    TEST: In the "List" tab / main screen, clicking on one of the 
    categories in the left column will cause only questions of that 
    category to be shown. 
    '''
    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        category = Category.query.filter(Category.id == category_id).one_or_none()

        if category is None:
            abort(404)
        
        all_questions = Question.query.filter(Question.category == category_id).all()
        questions = [question.format() for question in all_questions]

        return jsonify({
          'success': True,
          'questions': questions,
          'total_questions': len(questions),
          'current_category': category_id if category_id else None,
        })

    '''
    @TODO: 
    Create a POST endpoint to get questions to play the quiz. 
    This endpoint should take category and previous question parameters 
    and return a random questions within the given category, 
    if provided, and that is not one of the previous questions. 

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not. 
    '''
    @app.route('/quizzes', methods=['POST'])
    def get_quiz_questions():
        req = request.get_json()
        prev_questions = req.get('previous_questions')
        category = req.get('quiz_category')

        if category is None or prev_questions is None:
            abort(422)

        if category.get('id') != 0:
            question = Question.query.filter(
                          Question.category == category.get('id'),
                          Question.id.notin_(prev_questions)).order_by(func.random()).first()
        else:
            question = Question.query.filter(Question.id.notin_(prev_questions)).order_by(func.random()).first()

        if question:
            return jsonify({
              'success': True,
              'status_code': 200,
              'message': 'success',
              'question': question.format(),
            })
        else: 
            return jsonify({
              'success': True,
              'status_code': 200,
              'message': 'No more questions.' 
            })


    '''
    @TODO: 
    Create error handlers for all expected errors 
    including 404 and 422. 
    '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
          "success": False,
          "error": 404,
          "message": "Not found"
        }), 404
    
    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
          "success": False,
          "error": 422,
          "message": "Unprocessable Entity"
        }), 422

    return app
