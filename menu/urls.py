from django.urls import path
from . import views

urlpatterns = [
    path('create/menu_item/', views.create_menu),
]