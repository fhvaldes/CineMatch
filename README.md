
# CineMatch

CineMatch is a Django-based web application that allows users to sign up, log in, view and update their profiles, search for movies, and get movie recommendations based on their preferred genre. It also includes an API to list all movies.

## Features

- User signup, login, and logout
- User profile view and update
- Movie recommendations based on user preferences
- Home page with recommended movies
- Movie search functionality
- Movie detail view
- API to list all movies

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/fhvaldes31/CineMatch.git
    cd CineMatch
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Apply migrations:
    ```bash
    python manage.py migrate
    ```

5. Create a superuser:
    ```bash
    python manage.py createsuperuser
    ```

6. Run the development server:
    ```bash
    python manage.py runserver
    ```

## Running Tests

To run the tests, use the following command:
```bash
python manage.py test
```

## API Endpoints

- `GET /api/movies/` - List all movies

## Project Structure

- `movies/` - Contains the main application code
- `templates/` - Contains the HTML templates
- `static/` - Contains static files (CSS, JavaScript, images)
- `tests.py` - Contains the test cases for the application
- `urls.py` - Contains the URL configurations
- `views.py` - Contains the view functions

