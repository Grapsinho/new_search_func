from django.contrib import admin
from django.urls import path
from .views import ProductDetailAPIView, ProductInventoryApi

urlpatterns = [
    path('products/all', ProductInventoryApi.as_view()),
    path('products/<str:search>', ProductDetailAPIView.as_view()),
]
