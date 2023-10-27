from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name="users"),
    path('get-user-info/', views.get_user, name="get_user"),
    
]
