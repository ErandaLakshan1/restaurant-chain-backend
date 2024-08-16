from django.urls import path
from . import views

urlpatterns = [
    path('get_branches/', views.get_branches),
    path('get_branches/<int:pk>/', views.get_branches),

    path('add_branch/', views.create_branch),
    path('add_branch_images/<int:branch_id>/', views.add_images_to_branch),

    path('update_branch/<int:pk>/', views.update_branch),

    path('delete_branch/<int:pk>/', views.delete_branch),

    path('delete_branch_image/<int:image_id>/', views.delete_branch_image),
]