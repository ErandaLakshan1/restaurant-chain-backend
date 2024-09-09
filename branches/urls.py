from django.urls import path
from . import views

urlpatterns = [

    path('branches/', views.get_branches, name='get_branches'),
    path('branches/<int:pk>/', views.get_branches, name='get_branch'),


    path('branches/add/', views.create_branch, name='create_branch'),


    path('branches/<int:branch_id>/add-images/', views.add_images_to_branch, name='add_images_to_branch'),


    path('branches/<int:pk>/update/', views.update_branch, name='update_branch'),


    path('branches/<int:pk>/delete/', views.delete_branch, name='delete_branch'),


    path('branch-images/<int:image_id>/delete/', views.delete_branch_image, name='delete_branch_image'),
]
