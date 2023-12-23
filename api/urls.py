from django.contrib import admin
from django.urls import path
from .views import ProductDetailAPIView

urlpatterns = [
    # path('books/all', bookApi.as_view()),
    path('products/<str:search>', ProductDetailAPIView.as_view()),
]
