"""
Django admin configuration for blog models.
"""
from django.contrib import admin
from .models import Author, Post


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """Admin configuration for Author model."""
    list_display = ['name', 'email', 'created_at']
    search_fields = ['name', 'email']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Information', {
            'fields': ('name', 'email', 'bio')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Admin configuration for Post model."""
    list_display = ['title', 'author', 'status', 'views_count', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['title', 'content', 'author__name']
    readonly_fields = ['views_count', 'created_at', 'updated_at']
    fieldsets = (
        ('Content', {
            'fields': ('title', 'content', 'excerpt', 'author')
        }),
        ('Publishing', {
            'fields': ('status', 'published_at')
        }),
        ('Statistics', {
            'fields': ('views_count',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
