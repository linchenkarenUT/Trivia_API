import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random


from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
    @FINISHED
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    '''
    CORS(app)

    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )

        return response

    '''
    @Finished
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    '''
    @app.route("/categories", methods=["GET"])
    def show_categories():
        # return a list
        categories = Category.query.order_by(Category.id).all()
        data = {}

        if len(categories) == 0:
            abort(404)

        for cat in categories:
            data[cat.id] = cat.type

        return jsonify({
            'categories': data
        })

    '''
    @Finished
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
    def paginate_questions(request, selection):
        page = request.args.get("page", 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        questions = [question.format() for question in selection]
        categories = [question.get_category_name() for question in selection]
        current_questions = questions[start: end]
        current_categories = list(set(categories[start:end]))
        return current_questions, current_categories

    @app.route('/questions')
    def retrieve_questions():
        selection = Question.query.order_by(Question.id).all()

        current_questions, current_categories = paginate_questions(
            request, selection)
        categories = Category.query.order_by(Category.id).all()
        data = {}
        for cat in categories:
            data[cat.id] = cat.type

        if len(current_questions) == 0:
            abort(404)
        return jsonify({
            'questions': current_questions,
            'totalQuestions': len(selection),
            'categories': data,
            'currentCategory': current_categories
        })

    '''
    @Finished
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_book(question_id):
        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()
            if question is None:
                abort(404)
            question.delete()
            return jsonify({'status_code': 200, 'question': question.id})
        except BaseException:
            abort(422)

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
        body = request.get_json()

        try:
            new_question = body.get('question', None)
            new_answer = body.get('answer', None)
            new_difficulty = body.get('difficulty')
            new_category = body.get('category')
            searchTerm = body.get('searchTerm', None)

            if searchTerm:
                selection = Question.query.order_by(Question.id).filter(
                    Question.question.ilike("%{}%".format(searchTerm))
                ).all()
                current_questions, current_categories = paginate_questions(
                    request, selection)
                return jsonify({
                    'questions': current_questions,
                    'totalQuestions': len(selection),
                    'currentCategory': current_categories
                })

            else:
                if (not new_question) or (not new_answer):
                    abort(422)

                question = Question(
                    question=new_question,
                    answer=new_answer,
                    category=new_category,
                    difficulty=new_difficulty)
                question.insert()
                return jsonify({
                    'message': 'success'
                })
        except BaseException:
            abort(422)

    '''
    @Finished: look at above code
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    '''

    '''
    @Finished
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    '''
    @app.route('/categories/<int:category_id>/questions')
    def retrieve_category_questions(category_id):
        selection = Question.query.filter(
            Question.category == category_id).order_by(
            Question.id).all()
        if selection:
            current_questions, current_categories = paginate_questions(
                request, selection)

            return jsonify({
                'questions': current_questions,
                'totalQuestions': len(selection),
                'currentCategory': current_categories
            })
        else:
            abort(404)

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
    def get_one_quiz_question():
        body = request.get_json()
        try:
            previous_questions = body.get('previous_questions', [])
            quiz_category = body.get('quiz_category')
            if not quiz_category:
                abort(422)
            categoryId = int(quiz_category['id'])
            if categoryId == 0:
                question = Question.query.filter(
                    ~Question.id.in_(previous_questions)).first()
            else:
                question = Question.query.filter(
                    Question.category == categoryId) .filter(
                    ~Question.id.in_(previous_questions)).first()

            if not question:
                return jsonify({
                    'success': True, 'question': None
                })
            return jsonify({
                'success': True, 'question': question.format()
            })
        except BaseException:
            abort(422)

    '''
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    '''
    @app.errorhandler(400)
    def bad_request(error):
        return (jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400)

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({
                'success': False,
                'error': 404,
                'message': 'resource not found'
            }), 404)

    @app.errorhandler(422)
    def unprocessable(error):
        return (jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422)

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'internal server error'
        }), 500

    return app
