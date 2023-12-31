from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.get_products, name="products"),
    path('products/<str:pk>/', views.get_product, name="get_product_details"),
    path('products/delete/<str:pk>/', views.delete_product, name="delete_product_details")
]
