from django.contrib import admin
from django.urls import path
from .views import bookApi, BookDetailAPIView

urlpatterns = [
    path('books/all', bookApi.as_view()),
    path('books/<str:search>', BookDetailAPIView.as_view()),
]
