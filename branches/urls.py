from django.urls import path
from . import views

urlpatterns = [
    path('get_branches/', views.get_branches),
    path('get_branches/<int:pk>/', views.get_branches),
    path('add_branch/', views.create_branch),
]