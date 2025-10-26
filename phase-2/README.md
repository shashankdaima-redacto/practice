# Phase 2: Django Ninja REST API Project

A production-ready Django Ninja REST API project with comprehensive models and unit tests.

## Project Overview

This project demonstrates:
- **Django Models**: Author and Post with relationships and validation
- **Django Ninja APIs**: RESTful endpoints with automatic documentation
- **Unit Tests**: Comprehensive test coverage using pytest and pytest-django
- **Schemas**: Pydantic schemas for request/response validation

## Features

### Models
- **Author**: Represents blog post authors with name, email, and bio
- **Post**: Blog posts with title, content, status tracking, and view counting

### API Endpoints

#### Posts
- `GET /api/posts/` - List all posts (with optional filtering)
- `POST /api/posts/` - Create a new post
- `GET /api/posts/{post_id}/` - Get a specific post (increments view count)
- `PUT /api/posts/{post_id}/` - Update a post
- `DELETE /api/posts/{post_id}/` - Delete a post
- `GET /api/posts/{post_id}/increment-views/` - Increment post views

#### Authors
- `GET /api/posts/authors/` - List all authors
- `POST /api/posts/authors/` - Create a new author
- `GET /api/posts/authors/{author_id}/` - Get a specific author
- `PUT /api/posts/authors/{author_id}/` - Update an author
- `DELETE /api/posts/authors/{author_id}/` - Delete an author

### Query Parameters

#### Posts Filtering
- `status`: Filter by post status (draft, published, archived)
- `author_id`: Filter by author ID

## Setup

### Prerequisites
- Python 3.9+
- Poetry (package manager)

### Installation

1. Install dependencies:
```bash
poetry install
```

2. Activate the virtual environment:
```bash
poetry shell
```

3. Run database migrations:
```bash
python manage.py migrate
```

## Usage

### Running the Development Server

```bash
python manage.py runserver
```

The server will be available at `http://localhost:8000`

#### API Documentation
Visit `http://localhost:8000/api/docs/` for interactive API documentation

#### Health Check
```bash
curl http://localhost:8000/health/
```

### Creating Test Data

```bash
python manage.py shell

# Create an author
>>> from blog.models import Author
>>> author = Author.objects.create(name="John Doe", email="john@example.com", bio="A developer")

# Create a post
>>> from blog.models import Post
>>> post = Post.objects.create(
...     title="My First Post",
...     content="This is my first blog post",
...     author=author,
...     status="published"
... )
```

## Testing

### Run All Tests

```bash
pytest
```

### Run Specific Test Class

```bash
pytest blog/tests.py::TestPostModel
```

### Run Specific Test

```bash
pytest blog/tests.py::TestPostModel::test_create_post
```

### Run Tests with Coverage

```bash
pytest --cov=blog
```

### Run Tests with Verbose Output

```bash
pytest -v
```

## Test Coverage

The project includes comprehensive tests for:

### Model Tests
- Author model creation and validation
- Post model with relationships
- Foreign key constraints
- Default values and timestamps

### API Tests
- CRUD operations for Posts and Authors
- Filtering and querying
- Validation of request payloads
- Response structure validation
- View counting functionality

## Project Structure

```
phase-2/
├── config/
│   ├── __init__.py
│   ├── settings.py          # Django configuration
│   ├── urls.py              # URL routing and API setup
│   └── wsgi.py              # WSGI application
├── blog/
│   ├── __init__.py
│   ├── models.py            # Author and Post models
│   ├── schemas.py           # Pydantic schemas for validation
│   ├── api.py               # API endpoints
│   └── tests.py             # Unit tests
├── manage.py                # Django management script
├── pytest.ini               # Pytest configuration
├── pyproject.toml           # Poetry configuration
└── README.md                # This file
```

## API Examples

### Create an Author

```bash
curl -X POST http://localhost:8000/api/posts/authors/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Smith",
    "email": "jane@example.com",
    "bio": "A technical writer"
  }'
```

### Create a Post

```bash
curl -X POST http://localhost:8000/api/posts/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Getting Started with Django",
    "content": "Django is a powerful web framework...",
    "author_id": 1,
    "status": "published"
  }'
```

### List Posts with Filters

```bash
# Get all published posts
curl http://localhost:8000/api/posts/?status=published

# Get posts by specific author
curl http://localhost:8000/api/posts/?author_id=1
```

### Get a Post (increments view count)

```bash
curl http://localhost:8000/api/posts/1/
```

## Dependencies

### Core
- **django**: Web framework
- **django-ninja**: Modern REST API framework

### Development
- **pytest**: Testing framework
- **pytest-django**: Django integration for pytest
- **factory-boy**: Test fixtures
- **faker**: Fake data generation

## Notes

- All timestamps use UTC timezone
- Email addresses must be unique
- Posts default to 'draft' status
- Deleting an author cascades to delete their posts
- View counts are incremented only when fetching a post

## Next Steps

To extend this project, consider:
- Adding authentication and permissions
- Implementing pagination
- Adding search functionality
- Creating custom managers for common queries
- Adding API rate limiting
- Implementing caching strategies
