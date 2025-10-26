"""
API endpoints for the blog app using Django Ninja.
"""
from typing import List
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.pagination import paginate, PaginationBase
from ninja.errors import HttpError

from .models import Post, Author
from .schemas import (
    PostSchema, PostCreateSchema, PostUpdateSchema, PostListSchema,
    AuthorSchema, AuthorCreateSchema, AuthorUpdateSchema
)

router = Router()


# Author endpoints
@router.get("authors/", response=List[AuthorSchema], tags=["authors"])
def list_authors(request):
    """List all authors."""
    return Author.objects.all()


@router.get("authors/{author_id}/", response=AuthorSchema, tags=["authors"])
def get_author(request, author_id: int):
    """Get a specific author by ID."""
    author = get_object_or_404(Author, id=author_id)
    return author


@router.post("authors/", response=AuthorSchema, tags=["authors"])
def create_author(request, payload: AuthorCreateSchema):
    """Create a new author."""
    author = Author.objects.create(
        name=payload.name,
        email=payload.email,
        bio=payload.bio
    )
    return author


@router.put("authors/{author_id}/", response=AuthorSchema, tags=["authors"])
def update_author(request, author_id: int, payload: AuthorUpdateSchema):
    """Update an author."""
    author = get_object_or_404(Author, id=author_id)
    
    if payload.name is not None:
        author.name = payload.name
    if payload.bio is not None:
        author.bio = payload.bio
    
    author.save()
    return author


@router.delete("authors/{author_id}/", tags=["authors"])
def delete_author(request, author_id: int):
    """Delete an author."""
    author = get_object_or_404(Author, id=author_id)
    author.delete()
    return {"deleted": True, "id": author_id}


# Post endpoints
@router.get("", response=List[PostListSchema], tags=["posts"])
def list_posts(request, status: str = None, author_id: int = None):
    """
    List all posts with optional filtering.
    
    Query Parameters:
    - status: Filter by post status (draft, published, archived)
    - author_id: Filter by author ID
    """
    posts = Post.objects.all().select_related('author')
    
    if status:
        posts = posts.filter(status=status)
    if author_id:
        posts = posts.filter(author_id=author_id)
    
    return posts


@router.get("{post_id}/", response=PostSchema, tags=["posts"])
def get_post(request, post_id: int):
    """Get a specific post by ID."""
    post = get_object_or_404(Post, id=post_id)
    # Increment view count
    post.views_count += 1
    post.save(update_fields=['views_count'])
    return post


@router.post("", response=PostSchema, tags=["posts"])
def create_post(request, payload: PostCreateSchema):
    """Create a new post."""
    # Verify author exists
    author = get_object_or_404(Author, id=payload.author_id)
    
    post = Post.objects.create(
        title=payload.title,
        content=payload.content,
        excerpt=payload.excerpt,
        author=author,
        status=payload.status
    )
    return post


@router.put("{post_id}/", response=PostSchema, tags=["posts"])
def update_post(request, post_id: int, payload: PostUpdateSchema):
    """Update a post."""
    post = get_object_or_404(Post, id=post_id)
    
    if payload.title is not None:
        post.title = payload.title
    if payload.content is not None:
        post.content = payload.content
    if payload.excerpt is not None:
        post.excerpt = payload.excerpt
    if payload.status is not None:
        post.status = payload.status
    if payload.published_at is not None:
        post.published_at = payload.published_at
    
    post.save()
    return post


@router.delete("{post_id}/", tags=["posts"])
def delete_post(request, post_id: int):
    """Delete a post."""
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return {"deleted": True, "id": post_id}


@router.get("{post_id}/increment-views/", response=PostSchema, tags=["posts"])
def increment_post_views(request, post_id: int):
    """Increment the view count for a post."""
    post = get_object_or_404(Post, id=post_id)
    post.views_count += 1
    post.save(update_fields=['views_count'])
    return post
