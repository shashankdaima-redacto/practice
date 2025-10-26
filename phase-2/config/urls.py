"""
URL configuration for the project.
"""
from django.urls import path
from django.contrib import admin
from django.http import JsonResponse
from ninja import NinjaAPI

from blog.api import router

api = NinjaAPI(title="Blog API", description="A simple blog API with Django Ninja")
api.add_router("posts/", router, tags=["posts"])


def health_check(request):
    """Health check endpoint."""
    return JsonResponse({"status": "healthy"})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
    path("health/", health_check),
]
