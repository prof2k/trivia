# Full Stack Trivia API Backend

## Getting Started

- Base URL: http://127.0.0.1:5000/
- API Keys: None used

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

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
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle GET requests for all available categories.
4. Create an endpoint to DELETE question using a question ID.
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score.
6. Create a POST endpoint to get questions based on category.
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422 and 500.

## API Endpoints

```
Endpoints
GET '/categories'
GET '/questions'
DELETE '/questions'
POST '/questions'
POST '/play'


GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs.
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

GET '/questions?'
- Fetches a list of questions depending on the parameters specified in the query
- All questions are paginated into batches of 10s. See 'page' parameter below to see how it works
- Parameters: [Optional] 'q' ,'cat', 'page'
    - Parameter 'q'
    	- Value type = string
  		- It is used for search queries
  		- Can't be used with the 'cat' parameter
        - Returns an object containing questions (paginated into 10s) that matches the query string along with the status message and the total number of questions found

        Test Sample
        GET '/questions?q=title'
        Result: {
		  "questions": [
		    {
		      "answer": "Edward Scissorhands",
		      "category": 5,
		      "difficulty": 3,
		      "id": 6,
		      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
		    }
		  ],
		  "success": true,
		  "total_questions": 1
		}

	- Parameter 'cat'
		- Value type = integer
		- It is used to get questions that belong to only one category
		- Can't be used with the 'q' parameter
		- A successful query using it will return an object containing questions (paginated into 10s) that belong to that category and other useful metrics [see test sample below]

		Test Sample
		GET '/questions?cat=2'
		Result: {
		  "current_category": 2,
		  "questions": [
		    {
		      "answer": "Escher",
		      "category": 2,
		      "difficulty": 1,
		      "id": 16,
		      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
		    }, ...
		   ],
		  "success": true,
		  "total_questions": 4
		}

	- Parameter 'page'
		- Value type = integer
		- It is used to get the required paginated list of questions.
		- The value it is set to determines the set of questions it will show
		- It has a default value of 1
		- A successful query using it will return an object containing questions (paginated into 10s) depending on the value it is set and other useful metrics [see test sample below]

		Test Sample
		GET '/questions?page=2'
		Result: {
		  "questions": [
		    {
		      "answer": "Escher",
		      "category": 2,
		      "difficulty": 1,
		      "id": 16,
		      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
		    }, ...
		   ],
		   "categories": {
			    "1": "Science",
			    "2": "Art",
			    "3": "Geography",
			    "4": "History",
			    "5": "Entertainment",
			    "6": "Sports"
			},
			"current_category": 0,
		  	"success": true,
		  	"total_questions": 19
		}


DELETE '/questions/{question_id}'
- Deletes the question of specified id from the database
- A succesful query with it should return an object containing a success value set to true
Test Sample:
	DELETE /questions/2
	Result: {
      "success": True
    }

POST '/questions'
- Adds a question to the database
- Headers requuired: 'Content-Type'
- Returns the and object containing the question and a success value
Test Sample:
	POST '/questions'
	body = {
	  	"question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
      	"answer": "Edward Scissorhands",
      	"category": 5,
	  	"difficulty": 3
	}


	Result: {
		  "success": True,
		  "question": {
		  "id": 29,
		  "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?",
		  "answer": "Edward Scissorhands",
      	  "category": 5,
	  	  "difficulty": 3,
		}
	}

POST '/play'
- To play a quiz
- Takes two arguments - category id and list of previous questions ids received
- Each call returns a random question in the category requested (or all categories if category_id is set to 0) which doesn't match any id in list of previous question ids passed as an argument. This make sure that each call return a 'new' question.
Test Sample:
	POST '/questions'
	body = {
		"quiz_category": {
			"id": 1
			"type": "Science"
			},
		"previous_questions: [21, 20]
	}

	Result: {
		"success": True,
		"question": {
			"id": 29,
		  	"answer": "Boring Of Course", 
			"category": 1, 
			"difficulty": 5, 
			"id": 24, 
			"question": "Some incredibly boring question"
		}
	}


```

## Error types

- 404 : Resource not found

```
Sample Result : {
  "message": "Resource Not Found",
  "success": false
}
```

- 405 : Method not allowed - you should check you query method and the endpoint

```
Sample Result : {
  "message": "Method not allowed",
  "success": false
}
```

- 400 : Bad Request - you should check the body of your request for errors

```
Sample Result : {
  "message": "Method not allowed",
  "success": false
}
```

- 422 : Unprocessable - request valid but server can process it for some reason

```
Sample Result : {
  "message": "Unprocessable",
  "success": false
}
```

- 500 : [RARE] Something when wrong in the server while trying to execute the request

```
Sample Result : {
  "message": "Unprocessable",
  "success": false
}
```

## Testing

To run the tests, run

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
