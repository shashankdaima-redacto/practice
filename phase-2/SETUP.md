# Setup Instructions

Complete guide to set up the Django Ninja Blog API project.

## Option 1: Using Poetry (Recommended)

Poetry provides better dependency management and reproducibility.

### Prerequisites
- Python 3.9 or higher
- Poetry installed (`pip install poetry`)

### Steps

1. **Navigate to the project directory**
   ```bash
   cd phase-2
   ```

2. **Install dependencies**
   ```bash
   poetry install
   ```

3. **Activate the virtual environment**
   ```bash
   poetry shell
   ```

4. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Verify installation**
   ```bash
   pytest --version
   python manage.py --version
   ```

## Option 2: Using pip and requirements.txt

Use this if you prefer standard pip installation.

### Prerequisites
- Python 3.9 or higher
- pip and virtualenv

### Steps

1. **Navigate to the project directory**
   ```bash
   cd phase-2
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   ```bash
   # On macOS/Linux
   source venv/bin/activate
   
   # On Windows
   venv\Scripts\activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Verify installation**
   ```bash
   pytest --version
   python manage.py --version
   ```

## Verification Steps

After setup, verify everything works:

### 1. Run the test suite
```bash
pytest -v
```

Expected output: All tests should pass (30+ tests)

### 2. Start the development server
```bash
python manage.py runserver
```

Expected output:
```
Starting development server at http://127.0.0.1:8000/
```

### 3. Test the API
In another terminal:
```bash
curl http://localhost:8000/health/
```

Expected output:
```json
{"status": "healthy"}
```

### 4. Visit the documentation
Open in your browser: http://localhost:8000/api/docs/

You should see the interactive API documentation.

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'django'"
**Solution**: Make sure you've activated the virtual environment and installed dependencies.

```bash
# With Poetry
poetry shell
poetry install

# With pip
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: "No such table: django_migrations"
**Solution**: Run migrations first.

```bash
python manage.py migrate
```

### Issue: Port 8000 already in use
**Solution**: Use a different port.

```bash
python manage.py runserver 8001
```

### Issue: pytest not found
**Solution**: Install development dependencies.

```bash
# With Poetry
poetry install

# With pip
pip install -r requirements.txt
```

### Issue: Database locked error
**Solution**: This sometimes happens with SQLite. Try removing the database and migrating again.

```bash
rm db.sqlite3
python manage.py migrate
```

## Environment Variables (Optional)

Create a `.env` file for local configuration:

```bash
# .env
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
```

The project uses `python-dotenv` to load these variables.

## Quick Development Commands

```bash
# Run all tests
pytest

# Run tests with verbose output
pytest -v

# Run specific test class
pytest blog/tests.py::TestPostModel

# Run tests with coverage
pytest --cov=blog

# Start Django shell
python manage.py shell

# Create database migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Run development server on different port
python manage.py runserver 0.0.0.0:8001
```

## Next Steps

1. **Explore the code**: Review `blog/models.py` and `blog/api.py`
2. **Run tests**: Execute `pytest -v` to see all tests
3. **Start the server**: Run `python manage.py runserver`
4. **Try the API**: Visit http://localhost:8000/api/docs/
5. **Create data**: Use the API to create authors and posts
6. **Read documentation**: Check README.md and QUICKSTART.md

## Project Files Overview

- `manage.py` - Django management script
- `pyproject.toml` - Poetry configuration
- `requirements.txt` - pip dependencies
- `pytest.ini` - pytest configuration
- `conftest.py` - pytest fixtures
- `blog/models.py` - Database models
- `blog/api.py` - API endpoints
- `blog/tests.py` - Test suite
- `blog/schemas.py` - Data validation
- `config/settings.py` - Django settings
- `config/urls.py` - URL routing

## Support

For issues or questions:
1. Check the README.md file
2. Review the QUICKSTART.md guide
3. Look at the test files for usage examples
4. Check Django Ninja documentation: https://django-ninja.rest-framework.com/

Happy coding! 🚀
