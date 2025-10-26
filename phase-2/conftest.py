"""
Pytest configuration and fixtures for the project.
"""
import os
import django
import pytest

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    """
    Setup Django test database.
    """
    with django_db_blocker.unblock():
        from django.core.management import call_command
        call_command('migrate', verbosity=0)


@pytest.fixture
def client():
    """Provide a Django test client."""
    from django.test import Client
    return Client()


@pytest.fixture
def author_factory():
    """Factory fixture for creating test authors."""
    from blog.models import Author
    
    def create_author(name="Test Author", email="test@example.com", bio="Test bio"):
        return Author.objects.create(
            name=name,
            email=email,
            bio=bio
        )
    
    return create_author


@pytest.fixture
def post_factory(author_factory):
    """Factory fixture for creating test posts."""
    from blog.models import Post
    
    def create_post(
        title="Test Post",
        content="Test content",
        author=None,
        status="draft",
        excerpt=None
    ):
        if author is None:
            author = author_factory()
        
        return Post.objects.create(
            title=title,
            content=content,
            excerpt=excerpt,
            author=author,
            status=status
        )
    
    return create_post
