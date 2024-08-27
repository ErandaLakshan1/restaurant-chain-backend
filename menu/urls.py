from django.urls import path
from . import views

urlpatterns = [
    path('create/menu_item/', views.create_menu),

    path('get/menu_items/', views.get_menu_items),
    path('get/menu_item/<int:pk>/', views.get_menu_items),
    path('get/menu_item_by_user/<int:branch_id>/<int:pk>/', views.get_meu_items_according_to_branch),
    path('get/menu_items_by_user/<int:branch_id>/', views.get_meu_items_according_to_branch),
]