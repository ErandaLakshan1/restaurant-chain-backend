from django.urls import path
from . import views

urlpatterns = [
    path('create/coupon/', views.create_coupons),
    path('get/coupons/', views.get_coupons),
    path('get/coupon/<int:pk>/', views.get_coupons),

    path('update/coupon/<int:pk>/', views.update_coupons),
    path('delete/coupon/<int:pk>/', views.delete_coupons),

]
