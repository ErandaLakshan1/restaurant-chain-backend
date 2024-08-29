from django.urls import path
from . import views

urlpatterns = [
    path('create/coupon/', views.create_coupons),
    path('get/coupons/', views.get_coupons),
    path('get/coupon/<int:pk>/', views.get_coupons),

    path('update/coupon/<int:pk>/', views.update_coupons),
    path('delete/coupon/<int:pk>/', views.delete_coupons),

    path('create/cart/', views.add_items_to_cart),

    path('update/cart/<int:pk>/', views.update_items_in_cart),

    path('get/cart/', views.get_cart),

    path('delete/cart_item/<int:pk>/', views.delete_cart_item),
    path('delete/cart/', views.delete_cart),

    path('create/order/', views.place_order),

    path('get/ordres_by_admin_according_branches/<int:branch_id>/', views.get_placed_orders),
    path('get/ordre_by_admin_according_branche/<int:branch_id>/<int:pk>/', views.get_placed_orders),


    path('get/order_histroy_by_user/', views.get_the_order_history),
    path('get/order_histroy_by_user/<int:pk>/', views.get_the_order_history),


]
