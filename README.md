# Full Stack API Final Project


## Full Stack Trivia
In order to play the game, please clone the repo to local and run the backend and frontend

# API Reference
## Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://127.0.0.1:5000/, which is set as a proxy in the frontend configuration.
- Authentication: This version of the application does not require authentication or API keys.

## Error Handling
Errors are returned as JSON objects in the following format:
```
{
    'success': False,
    'error': 404,
    'message': 'resource not found'
}
```
The API will return two error types when requests fail:
- 400: bad request
- 404: Resource Not Found
- 422: Not Processable

## Endpoints
### GET /questions
- General
    - return a list of question objects, number of total questions, all categories, and list of categories of current questions.
    - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
- Sample: ```curl http://127.0.0.1:5000/questions```
    ```
    {
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "currentCategory": [
    "Art", 
    "Entertainment", 
    "Geography", 
    "History", 
    "Sports"
  ], 
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }, 
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }, 
    {
      "answer": "Escher", 
      "category": 2, 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }
  ], 
  "totalQuestions": 22}
  ```

### GET /categories
- General: 
    - return a list of categories
- Sample: ```curl http://127.0.0.1:5000/categories```
    ```
    {
        "categories": {
            "1": "Science", 
            "2": "Art", 
            "3": "Geography", 
            "4": "History", 
            "5": "Entertainment", 
            "6": "Sports"
        }
    }
    ```

### DELETE /questions/{question_id}
- General
    - Delete the question of the given ID if it exists. Return the status_code 200 if delete is finished. Refresh the List page then the question is gone.
- Sample: ```curl -X DELETE http://127.0.0.1:5000/questions/5```
    ```
    {
        "status_code": 200
    }
    ```

### POST /questions
- General
    - Create a new trivia question given the question text and answer text.
    - return the message `success` if the trivia question has been successfully created
- Sample: ```curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question": "what is Toyota?", "answer": "auto brand", "difficulty": 1, "category":1}'```
    ```
    {
    "message": "success"
    }
    ```

### POST /categories/{category_id}/questions
- General
    - Return a list of questions object based on the category_id, how many questions are in this category, and current category name
- sample: ```curl http://127.0.0.1:5000/categories/1/questions```
    ```
    {
    "currentCategory": [
        "Science"
    ], 
    "questions": [
        {
        "answer": "The Liver", 
        "category": 1, 
        "difficulty": 4, 
        "id": 20, 
        "question": "What is the heaviest organ in the human body?"
        }, 
        {
        "answer": "Alexander Fleming", 
        "category": 1, 
        "difficulty": 3, 
        "id": 21, 
        "question": "Who discovered penicillin?"
        }, 
        {
        "answer": "Blood", 
        "category": 1, 
        "difficulty": 4, 
        "id": 22, 
        "question": "Hematology is a branch of medicine involving the study of what?"
        }, 
        {
        "answer": "auto brand", 
        "category": 1, 
        "difficulty": 1, 
        "id": 29, 
        "question": "what is Toyota?"
        }
    ], 
    "totalQuestions": 4
    }
    ```

### POST /quizzes
- General
    - Take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
- Sample: ```curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [], "quiz_category": {"type": "science","id": "1"}}'```
    ```
    {
    "question": {
        "answer": "The Liver", 
        "category": 1, 
        "difficulty": 4, 
        "id": 20, 
        "question": "What is the heaviest organ in the human body?"
        }
    }
    ```
