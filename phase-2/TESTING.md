# Testing Guide

Complete guide to testing the Django Ninja Blog API project.

## Overview

The project includes 30+ comprehensive unit tests covering:
- Model creation and validation
- CRUD operations (Create, Read, Update, Delete)
- Query filtering
- API endpoint validation
- View counting functionality
- Relationship handling

## Test Structure

### Test Classes

1. **TestAuthorModel** - Tests for Author model
2. **TestPostModel** - Tests for Post model
3. **TestPostAPIs** - Tests for Post API endpoints
4. **TestAuthorAPIs** - Tests for Author API endpoints

### Test Files Location
- `blog/tests.py` - Main test file with all test classes
- `conftest.py` - Pytest fixtures and configuration

## Running Tests

### Run All Tests
```bash
pytest
```

Output:
```
collected 30 items
blog/tests.py::TestAuthorModel::test_create_author PASSED
blog/tests.py::TestAuthorModel::test_author_string_representation PASSED
blog/tests.py::TestAuthorModel::test_unique_email_constraint PASSED
blog/tests.py::TestAuthorModel::test_author_timestamps PASSED
blog/tests.py::TestPostModel::test_create_post PASSED
...
```

### Run Tests with Verbose Output
```bash
pytest -v
```

Shows more detail about each test.

### Run Specific Test Class
```bash
pytest blog/tests.py::TestPostModel
```

Runs only tests in the TestPostModel class.

### Run Specific Test
```bash
pytest blog/tests.py::TestPostModel::test_create_post
```

Runs only a single test.

### Run Tests with Coverage Report
```bash
pytest --cov=blog
```

Shows code coverage percentage.

### Run Tests and Show Only Failures
```bash
pytest -x
```

Stops at first failure.

### Run Tests with Short Traceback
```bash
pytest --tb=short
```

Easier to read error messages.

## Test Categories

### Model Tests (11 tests)

#### Author Model Tests (4 tests)
```python
def test_create_author()                  # Create author with valid data
def test_author_string_representation()   # Author __str__ method
def test_unique_email_constraint()        # Email uniqueness validation
def test_author_timestamps()              # created_at and updated_at fields
```

#### Post Model Tests (7 tests)
```python
def test_create_post()                    # Create post with valid data
def test_post_string_representation()     # Post __str__ method
def test_post_status_choices()            # Status field choices
def test_post_default_status()            # Default status value
def test_post_with_excerpt()              # Optional excerpt field
def test_post_timestamps()                # Timestamps functionality
def test_delete_author_deletes_posts()    # Cascade deletion
```

### API Tests (19 tests)

#### Post API Tests (10 tests)
```python
def test_list_posts_empty()               # List posts when none exist
def test_list_posts_with_data()           # List posts with data
def test_create_post()                    # POST /api/posts/
def test_get_post()                       # GET /api/posts/{id}/
def test_get_post_increments_views()      # View count increment
def test_update_post()                    # PUT /api/posts/{id}/
def test_delete_post()                    # DELETE /api/posts/{id}/
def test_filter_posts_by_status()         # Filter by status
def test_filter_posts_by_author()         # Filter by author_id
def test_increment_post_views()           # Dedicated view increment endpoint
```

#### Author API Tests (9 tests)
```python
def test_list_authors_empty()             # List authors when none exist
def test_list_authors()                   # List authors with data
def test_create_author()                  # POST /api/posts/authors/
def test_get_author()                     # GET /api/posts/authors/{id}/
def test_update_author()                  # PUT /api/posts/authors/{id}/
def test_delete_author()                  # DELETE /api/posts/authors/{id}/
```

## Test Examples

### Testing Model Creation
```python
@pytest.mark.django_db
def test_create_author():
    author = Author.objects.create(
        name="John Doe",
        email="john@example.com",
        bio="A great author"
    )
    assert author.id is not None
    assert author.name == "John Doe"
```

### Testing API Endpoints
```python
@pytest.mark.django_db
def test_create_post(self, client, author):
    payload = {
        "title": "New Post",
        "content": "New content",
        "author_id": author.id,
        "status": "draft"
    }
    response = client.post(
        "/api/posts/",
        data=payload,
        content_type="application/json"
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "New Post"
```

### Testing Query Filtering
```python
@pytest.mark.django_db
def test_filter_posts_by_status(self, client, author):
    Post.objects.create(
        title="Published",
        content="Content",
        author=author,
        status="published"
    )
    Post.objects.create(
        title="Draft",
        content="Content",
        author=author,
        status="draft"
    )
    response = client.get("/api/posts/?status=published")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["status"] == "published"
```

## Using Test Fixtures

The project includes pytest fixtures in `conftest.py`:

### Client Fixture
```python
def test_example(client):
    response = client.get("/api/posts/")
```

### Author Factory Fixture
```python
def test_example(author_factory):
    author = author_factory(name="Jane", email="jane@example.com")
```

### Post Factory Fixture
```python
def test_example(post_factory):
    post = post_factory(title="Test", status="published")
```

## Test Coverage Analysis

### Covered Areas
- ✅ Model field validation
- ✅ Model relationships
- ✅ Model constraints (unique, foreign keys)
- ✅ Model defaults
- ✅ Model timestamps
- ✅ API CRUD operations
- ✅ Query filtering
- ✅ Response format validation
- ✅ Status codes
- ✅ View counting

### Recommendations for Additional Tests

You can extend the test suite with:

```python
# Test invalid data
def test_create_author_invalid_email():
    with pytest.raises(Exception):
        Author.objects.create(
            name="John",
            email="invalid-email"
        )

# Test edge cases
def test_post_with_very_long_title():
    author = author_factory()
    post = Post.objects.create(
        title="x" * 200,
        content="Content",
        author=author
    )
    assert len(post.title) == 200

# Test permissions
def test_create_post_requires_auth():
    # After adding authentication
    response = client.post("/api/posts/")
    assert response.status_code == 401

# Test pagination
def test_list_posts_pagination():
    # After adding pagination
    response = client.get("/api/posts/?limit=10&offset=0")
    assert "count" in response.json()
```

## Debugging Tests

### Print debug information
```python
def test_example(client):
    response = client.get("/api/posts/")
    print(response.json())  # Add print statements
    assert response.status_code == 200
```

### Run with print output
```bash
pytest -s
```

The `-s` flag shows print statements.

### Run with full traceback
```bash
pytest --tb=long
```

### Use pdb for debugging
```python
def test_example(client):
    import pdb; pdb.set_trace()  # Debugger will stop here
    response = client.get("/api/posts/")
```

## Performance Testing

### Test execution time
```bash
pytest --durations=10
```

Shows the 10 slowest tests.

### Profile specific test
```bash
pytest blog/tests.py::TestPostModel::test_create_post -v --profile
```

## Continuous Integration

### Running tests in CI/CD
```bash
# Typical CI command
pytest --cov=blog --cov-report=xml --junitxml=junit.xml
```

## Common Testing Patterns

### Setup and Teardown
```python
@pytest.fixture
def setup_teardown():
    # Setup
    author = Author.objects.create(...)
    
    yield author  # Test runs here
    
    # Teardown
    author.delete()
```

### Multiple objects
```python
@pytest.mark.django_db
def test_with_multiple_authors():
    authors = [
        Author.objects.create(name=f"Author {i}", email=f"author{i}@example.com")
        for i in range(5)
    ]
    assert len(authors) == 5
```

### Testing exceptions
```python
def test_unique_constraint():
    Author.objects.create(name="John", email="john@example.com")
    with pytest.raises(IntegrityError):
        Author.objects.create(name="Jane", email="john@example.com")
```

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Pytest-Django Documentation](https://pytest-django.readthedocs.io/)
- [Django Testing Documentation](https://docs.djangoproject.com/en/4.2/topics/testing/)
- [Django Ninja Testing](https://django-ninja.rest-framework.com/guides/testing/)

## Quick Reference Commands

```bash
# All tests
pytest

# Verbose output
pytest -v

# Stop on first failure
pytest -x

# Show print output
pytest -s

# Coverage report
pytest --cov=blog

# Specific test
pytest blog/tests.py::TestPostModel::test_create_post

# Test a pattern
pytest -k "test_create"

# Last failed tests
pytest --lf

# Failed tests first
pytest --ff
```

Happy testing! 🧪
