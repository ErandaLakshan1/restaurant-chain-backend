from django.urls import path
from . import views

urlpatterns = [
    path('get/table_list/<int:branch_id>/', views.get_table_list),
    path('get/table_list/<int:branch_id>/<int:pk>/', views.get_table_list),

    path('create/table/', views.create_table),

    path('update/table/<int:pk>/', views.update_table_details),

    path('delete/table/<int:pk>/', views.delete_table),

    path('create/reservation/', views.make_reservation),

    path('get/reservations/', views.get_reservation_list),
    path('get/reservations_by_admins/', views.get_reservation_list_by_admins),
    path('get/reservation/<int:pk>/', views.get_reservation_list),

    path('update/reservation/<int:pk>/', views.update_reservation_details),
    path('delete/reservation/<int:pk>/', views.delete_reservation),


]