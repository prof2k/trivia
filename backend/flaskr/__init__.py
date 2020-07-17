import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_cors import cross_origin as origins
import random

from models import setup_db, Question, Category
import sys

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  # CORS(app)
  CORS(app, resources={r'/': {origins: '*'}})

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS')
    return response


  # To get categories
  @app.route('/categories')
  def get_categories():
    formated_categories = {}
    categories = Category.query.all();
    for category in categories:
      formated_categories[category.id] = category.type
    
    return jsonify({
      'success': True,
      'categories': formated_categories
    }), 200

  def paginate(list, page_no):
    start_val = (page_no - 1) * QUESTIONS_PER_PAGE
    end_val = start_val + QUESTIONS_PER_PAGE
    return list[start_val:end_val]

  # For search queries
  def search_questions(query, page):
    questions_found = Question.query.filter(Question.question.ilike(f'%{query}%')).all()
    sent_questions = paginate(questions_found, page)

    # If nothing is found (no matches)
    if not len(sent_questions):
      abort(404)

    sent_questions_formated = [question.format() for question in sent_questions]
    return jsonify({
      'success': True,
      'questions': sent_questions_formated,
      'total_questions': len(questions_found)
    }), 200


  # For By-Category queries
  def get_questions_by_category(id, page):
    id = id
    questions_found = Question.query.filter(Question.category == id).all()
    sent_questions = paginate(questions_found, page)

    # If nothing is found (no such category)
    if not len(sent_questions):
      abort(404)

    sent_questions_formated = [question.format() for question in sent_questions]
    return jsonify({
      'success': True,
      'questions': sent_questions_formated,
      'total_questions': len(questions_found),
      'current_category':  id
    }), 200

  # For search queries, by-category queries, and reqular queries of questions with pagination
  @app.route('/questions', methods=['GET'])
  def get_questions_with_pagination():
    search_query = request.args.get('q')
    category_id = request.args.get('cat')
    page = request.args.get('page', 1, type=int)

    # For operations containing both search and get-by-category
    if category_id and search_query:
      abort(405)


    # If it's a search query
    if search_query:
      return search_questions(search_query, page)

    # If it's a query by category
    elif category_id and category_id.isdigit():
      category_id = int(category_id)
      return get_questions_by_category(category_id, page)

    # If it's a reqular query
    else:
      all_questions = Question.query.all()
      sent_questions = paginate(all_questions, page)

      # If the page limit has been reached
      if not len(sent_questions):
        abort(404)
        
      formated_categories = {}
      categories = Category.query.all();
      for category in categories:
        formated_categories[category.id] = category.type
           

      sent_questions_formated = [question.format() for question in sent_questions]

      return jsonify({
        'success': True,
        'questions': sent_questions_formated,
        'total_questions': len(all_questions),
        'categories': formated_categories,
        'current_category':  0
      }), 200


  # To delete a question based on it's id
  @app.route('/questions/<int:id>', methods=['DELETE'])
  def delete_question(id):
    try:
      question = Question.query.get(id).delete()
    except:
      abort(404)

    return jsonify({
      'success': True
    }), 200


  # To add a new question
  @app.route('/questions', methods=['POST'])
  def add_question():
    data = request.get_json()
    try:
      new_question = Question(
        question = data.get('question'),
        answer = data.get('answer'),
        category = data.get('category'),
        difficulty = data.get('difficulty', 1)
      )
      new_question.insert()
    except:
      abort(400)
    return jsonify({
      'success': True,
      'question': new_question.format()
    }), 200


  # To play the quiz
  @app.route('/play', methods=['POST'])
  def get_random_question():
    category = request.get_json()['quiz_category']['id']
    previous_questions = request.get_json()['previous_questions']

    try:
        def still_left(list):
            if len(previous_questions) <= len(list):
                return True
            else:
                return False
      
        # To get all questions irrespective of category
        if category == 0:
            questions = Question.query.all()
            
            # If the all items in the list have been used up
            if still_left(questions):
                filtered_questions = list(filter(
                    lambda question: (question.id not in previous_questions)
                    , questions))
                question = random.choice(filtered_questions)
                
            else:
                return jsonify({
                    'success': True
                })
        # To get questions by category
        else: 
            questions = Question.query.filter(Question.category == category).all()
            
            # If the all items in the list have been used up
            if still_left(questions): 
                filtered_questions = list(filter(
                lambda question: (question.id not in previous_questions)
                , questions))
                question = random.choice(filtered_questions)
            else: 
                abort(404)
                return jsonify({
                    'success': True
                })
                
        return jsonify({
            'success': True,
            'question': question.format()
         })
    except:
        print(sys.exc_info())
        abort(400)            
        
        
  # Error handlers
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success': False,
      'message': 'Resource Not Found'
    }), 404

  @app.errorhandler(405)
  def not_found(error):
    return jsonify({
      'success': False,
      'message': 'Method not allowed'
    }), 404

  @app.errorhandler(400)
  def not_found(error):
    return jsonify({
      'success': False,
      'message': 'Bad Request'
    }), 400

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      'success': False,
      'message': 'Unprocessable'
    }), 422
  
  return app

    