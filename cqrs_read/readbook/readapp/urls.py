from django.urls import path
from .views import bookAPI

urlpatterns = [
    path("books/", bookAPI)
]