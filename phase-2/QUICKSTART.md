# Quick Start Guide

Get up and running with the Django Ninja Blog API in minutes!

## 1. Install Dependencies

```bash
cd phase-2
poetry install
poetry shell
```

## 2. Setup Database

```bash
python manage.py migrate
```

## 3. Run Tests

```bash
# All tests
pytest

# With verbose output
pytest -v

# Specific test class
pytest blog/tests.py::TestPostModel
```

## 4. Start Development Server

```bash
python manage.py runserver
```

## 5. Access the Application

- **API**: http://localhost:8000/api/
- **API Docs**: http://localhost:8000/api/docs/
- **Admin Panel**: http://localhost:8000/admin/
- **Health Check**: http://localhost:8000/health/

## 6. Create Test Data via API

### Create an Author
```bash
curl -X POST http://localhost:8000/api/posts/authors/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Developer",
    "email": "john@dev.com",
    "bio": "A passionate developer"
  }'
```

### Create a Post
```bash
curl -X POST http://localhost:8000/api/posts/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First Blog Post",
    "content": "This is an amazing post about Django",
    "excerpt": "Learn Django basics",
    "author_id": 1,
    "status": "published"
  }'
```

### List All Posts
```bash
curl http://localhost:8000/api/posts/
```

### Get Specific Post
```bash
curl http://localhost:8000/api/posts/1/
```

### Update a Post
```bash
curl -X PUT http://localhost:8000/api/posts/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Post Title"
  }'
```

### Delete a Post
```bash
curl -X DELETE http://localhost:8000/api/posts/1/
```

## Test Files Overview

- **blog/models.py**: Author and Post models
- **blog/schemas.py**: Pydantic validation schemas
- **blog/api.py**: API endpoints
- **blog/tests.py**: Comprehensive test suite
  - `TestAuthorModel`: Model tests
  - `TestPostModel`: Model tests
  - `TestPostAPIs`: API endpoint tests
  - `TestAuthorAPIs`: Author API endpoint tests

## Test Coverage

The project includes 30+ unit tests covering:
- ✅ Model creation and validation
- ✅ CRUD operations
- ✅ Filtering and querying
- ✅ View counting
- ✅ Foreign key relationships
- ✅ Cascade deletion

## Useful Commands

```bash
# Enter Django shell
python manage.py shell

# Create database migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run specific test with coverage
pytest blog/tests.py::TestPostAPIs::test_create_post -v

# Run tests and show which ones failed
pytest -v --tb=short
```

## Project Structure

```
├── blog/
│   ├── models.py      # ORM models
│   ├── schemas.py     # Data validation
│   ├── api.py         # API endpoints
│   ├── tests.py       # Test suite
│   └── admin.py       # Admin config
├── config/
│   ├── settings.py    # Django config
│   ├── urls.py        # URL routing
│   └── wsgi.py        # WSGI app
├── manage.py          # Django CLI
├── pytest.ini         # Pytest config
├── pyproject.toml     # Poetry config
└── README.md          # Full documentation
```

## Next Steps

1. Run all tests: `pytest -v`
2. Start server: `python manage.py runserver`
3. Visit API docs: http://localhost:8000/api/docs/
4. Create data via API and test endpoints
5. Write additional tests for custom features

Happy coding! 🚀
