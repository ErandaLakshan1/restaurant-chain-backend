from django.urls import path
from . import views

urlpatterns = [
    path('get/table_list/<int:branch_id>/', views.get_table_list),
    path('get/table_list/<int:branch_id>/<int:pk>/', views.get_table_list),

    path('create/table/', views.create_table),

    path('update/table/<int:pk>/', views.update_table_details),

    path('delete/table/<int:pk>/', views.delete_table),
]