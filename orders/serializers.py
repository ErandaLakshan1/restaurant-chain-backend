from rest_framework import serializers
from .models import Order, Coupon, Cart, CartItem, OrderItem
from menu.serializers import MenuSerializer


class CartItemSerializer(serializers.ModelSerializer):
    menu_item = MenuSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'menu_item', 'quantity', 'added_at']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, source='cartitem_set')

    class Meta:
        model = Cart
        fields = ['id', 'user', 'branch', 'items', 'created_at', 'updated_at']


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ['id', 'code', 'discount_percentage', 'expiration_date']


class OrderItemSerializer(serializers.ModelSerializer):
    menu_item = MenuSerializer()

    class Meta:
        model = OrderItem
        fields = ['menu_item', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    coupon = CouponSerializer(read_only=True)
    order_items = OrderItemSerializer(many=True)
    customer_first_name = serializers.SerializerMethodField()
    customer_last_name = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id', 'customer_first_name', 'customer_last_name', 'branch', 'delivery_partner', 'order_type',
            'status', 'order_items', 'coupon', 'total_price', 'discount_applied', 'final_price', 'created_at'
        ]

    def get_customer_first_name(self, obj):
        return obj.customer.first_name

    def get_customer_last_name(self, obj):
        return obj.customer.last_name