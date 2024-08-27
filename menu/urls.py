from django.urls import path
from . import views

urlpatterns = [
    path('create/menu_item/', views.create_menu),

    path('get/menu_items/', views.get_menu_items),
    path('get/menu_item/<int:pk>/', views.get_menu_items),

]