from django.contrib import admin
from .models import Coupon, Order, Cart, CartItem

# Register your models here.
admin.site.register(Coupon)
admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(CartItem)