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

    
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

  
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-type, Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        return response
    

    
    @app.route('/categories')
    def get_categories():
        categories = Category.query.all()
        categories_response = [category.format() for category in categories]
        return jsonify({
            'status_code': 200,
            'success': True,
            'data': categories_response,
        })


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
      Error Handlers
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
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
          "success": False,
          "error": 400,
          "message": "Bad Request"
        }), 400
    
    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
          "success": False,
          "error": 500,
          "message": "Internal Server Error"
        }), 500


    return app
