"""
Pydantic schemas for API validation and serialization.
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr


class AuthorSchema(BaseModel):
    """Schema for Author serialization."""
    id: int
    name: str
    email: str
    bio: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AuthorCreateSchema(BaseModel):
    """Schema for creating a new Author."""
    name: str
    email: EmailStr
    bio: Optional[str] = None


class AuthorUpdateSchema(BaseModel):
    """Schema for updating an Author."""
    name: Optional[str] = None
    bio: Optional[str] = None


class PostSchema(BaseModel):
    """Schema for Post serialization with author info."""
    id: int
    title: str
    content: str
    excerpt: Optional[str] = None
    author: AuthorSchema
    status: str
    created_at: datetime
    updated_at: datetime
    published_at: Optional[datetime] = None
    views_count: int

    class Config:
        from_attributes = True


class PostCreateSchema(BaseModel):
    """Schema for creating a new Post."""
    title: str
    content: str
    excerpt: Optional[str] = None
    author_id: int
    status: str = 'draft'


class PostUpdateSchema(BaseModel):
    """Schema for updating a Post."""
    title: Optional[str] = None
    content: Optional[str] = None
    excerpt: Optional[str] = None
    status: Optional[str] = None
    published_at: Optional[datetime] = None


class PostListSchema(BaseModel):
    """Schema for Post list without full author details."""
    id: int
    title: str
    excerpt: Optional[str] = None
    author: AuthorSchema
    status: str
    created_at: datetime
    published_at: Optional[datetime] = None
    views_count: int

    class Config:
        from_attributes = True
