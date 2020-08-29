# Full Stack Trivia API Backend

## Getting Started

### Pre-requisites

In order to run this project properly, make sure you have the following installed:
  * Python 3
  * Flask
  * SQL Alchemy
  * Flask-CORS

## Initial Setup (Windows Based)
  1. First create a table called trivia using a 'postgres' user. 
  2. If would like to test the app with fake data:
      ```
      psql -U postgres -f trivia.psql -d trivia
      ```
  3. Set up the environment:
      ```
      $env:FLASK_ENV = "development"
      ```
  4. Set up the Flask App:
      ```
      $env:FLASK_APP = "flaskr"
      ```
  5. Run the app:
      ```
      flask run
      ```

## API Reference
 * As mentioned at the Project Documentation README, this project was intended to run locally, thus the backend is hosted at the default ```http://127.0.0.1:5000/```, also set as a proxy in the frontend configuration.
 * Authentication: This application does not require any type of authentication or API key.

### Error Handling
The errors in this application are returned as JSON objects in the following format:
```
        {
          "success": False,
          "error": 404,
          "message": "Not found"
        }
```

This API handles the following errors:
* 400 - Bad Request
* 404 - Not Found
* 422 - Unprocessable Entity
* 500 - Internal Server Error


### Endpoints

#### GET /categories

- Fetches an array of categories in with ids and types
- Request Arguments: None
- Returns: An array of objects (categories), which contains a object of id: category_string key:value pairs and type.

Test it with curl:
```
curl  http://127.0.0.1:5000/categories
```

Sample Response: 

```
 {"data":[{"id":1,"type":"Science"},
          {"id":2,"type":"Art"},
          {"id":3,"type":"Geography"},
          {"id":4,"type":"History"},
          {"id":5,"type":"Entertainment"},
          {"id":6,"type":"Sports"}],
  "status_code":200,
  "success":true
 }
```

#### GET /questions

- Fetches an array of questions and an array with categories
- Request Arguments: Page (Optional)
- Returns: An array of categories, an array of questions, the total number of questions, and the current_category

Test it with curl:
```
curl  http://127.0.0.1:5000/questions?page=2
```

Sample Response:
```
{
    "categories": [
        {
            "id": 1,
            "type": "Science"
        },
        ...
    ],
    "current_category": null,
    "questions": [
        {
            "answer": "Jackson Pollock",
            "category": 2,
            "difficulty": 2,
            "id": 19,
            "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
        },
        ...
    ],
    "status_code": 200,
    "success": true,
    "total_questions": 19
}
```
#### DELETE /questions/<int:question_id>

- Fetches an specific question and deletes it.
- Request Arguments: An integer for question id.
- Returns: An array of categories, an array of questions, the total number of questions, and the current_category

Test it with curl:
```
curl -X DELETE http://127.0.0.1:5000/questions/18
```

Sample Response:
```
{
  "deleted": 18,
  "message": "The question was successfully deleted.",
  "status_code": 200,
  "success": true
}
```

#### POST /questions

- Creates an specific question.
- Request Arguments: A JSON object with a question, an answer, a difficulty, and a category.
- Returns: The created question successfully formatted.

Test it with curl:
```
curl -X POST  -d '{\"question\":\"Who played Forest in Forest Gump?\",\"answer\":\"Tom Henkins\",\"category\":\"2\",\"difficulty\":\"2\"}'  -H "Content-Type: application/json"  http://127.0.0.1:5000/questions
```
Sample Response:
```
{
  "message": "The question was successfully created",
  "question": {
    "answer": "Henkins",
    "category": 2,
    "difficulty": 2,
    "id": 38,
    "question": "Tom"
  },
  "status_code": 200,
  "success": true
}
```
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 




### Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
