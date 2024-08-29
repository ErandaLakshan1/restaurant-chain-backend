from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from . import models
from . import serializers
from branches.models import Branch
from menu.models import Menu
from .models import Coupon


# Create your views here.
# to add coupons
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_coupons(request, *args, **kwargs):
    user = request.user
    user_type = getattr(user, 'user_type')

    if user_type != 'admin':
        return Response({"detail: You do not have permission to perform this actions."},
                        status=status.HTTP_403_FORBIDDEN)

    serializer = serializers.CouponSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"detail": "Coupon added successfully.", "data": serializer.data},
                        status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# to get all the coupons and the selected coupon
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_coupons(request, pk=None, *args, **kwargs):
    if pk:
        try:
            coupon = models.Coupon.objects.get(pk=pk)
            serializer = serializers.CouponSerializer(coupon)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except models.Coupon.DoesNotExist:
            return Response({"detail": "Coupon does not exist."}, status=status.HTTP_404_NOT_FOUND)

    coupons = models.Coupon.objects.all()
    serializer = serializers.CouponSerializer(coupons, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# to update the coupons
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_coupons(request, pk, *args, **kwargs):
    user = request.user
    user_type = getattr(user, 'user_type')

    if user_type != 'admin':
        return Response({"detail: You do not have permission to perform this actions."},
                        status=status.HTTP_403_FORBIDDEN)

    try:
        coupon = models.Coupon.objects.get(pk=pk)
    except models.Coupon.DoesNotExist:
        return Response({"detail": "Coupon does not exist."}, status=status.HTTP_404_NOT_FOUND)

    serializer = serializers.CouponSerializer(coupon, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"detail": "Coupon updated successfully.", "data": serializer.data}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# to delete coupons
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_coupons(request, pk, *args, **kwargs):
    user = request.user
    user_type = getattr(user, 'user_type')

    if user_type != 'admin':
        return Response({"detail: You do not have permission to perform this actions."},
                        status=status.HTTP_403_FORBIDDEN)

    try:
        coupon = models.Coupon.objects.get(pk=pk)
    except models.Coupon.DoesNotExist:
        return Response({"detail": "Coupon does not exist."}, status=status.HTTP_404_NOT_FOUND)

    coupon.delete()
    return Response({"detail": "Coupon deleted successfully."}, status=status.HTTP_200_OK)


# to add items to cart
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_items_to_cart(request, *args, **kwargs):
    user = request.user
    items = request.data.get('items')
    branch_id = request.data.get('branch')

    if not branch_id:
        return Response({"detail": "Branch ID is required"}, status=status.HTTP_400_BAD_REQUEST)

    if not items or not isinstance(items, list):
        return Response({"detail": "Items are required and should be a list"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        branch = Branch.objects.get(id=branch_id)
    except Branch.DoesNotExist:
        return Response({"detail": "Branch not found"}, status=status.HTTP_404_NOT_FOUND)

    cart, created = models.Cart.objects.get_or_create(user=user, branch=branch)

    if cart.is_expired():
        cart.delete()
        cart = models.Cart.objects.get_or_create(user=user, branch=branch)

    cart_items = []
    for item in items:
        menu_item_id = item.get('menu_item')
        quantity = item.get('quantity')

        try:
            menu_item = Menu.objects.get(id=menu_item_id)
        except Menu.DoesNotExist:
            return Response({"detail": f"Menu item with id {menu_item_id} not found"}, status=status.HTTP_404_NOT_FOUND)

        cart_item, created = models.CartItem.objects.get_or_create(cart=cart, menu_item=menu_item)
        cart_item.quantity = int(quantity)
        cart_item.save()

        cart_items.append(cart_item)

    serializer = serializers.CartItemSerializer(cart_items, many=True)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


# to update the cart items
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_items_in_cart(request, pk, *args, **kwargs):
    try:
        cart_item = models.CartItem.objects.get(pk=pk, cart__user=request.user)
    except models.CartItem.DoesNotExist:
        return Response({"detail": "Cart item does not exist."}, status=status.HTTP_404_NOT_FOUND)

    quantity = request.data.get('quantity', cart_item.quantity)
    cart_item.quantity = int(quantity)
    cart_item.save()

    serializer = serializers.CartItemSerializer(cart_item)
    return Response(serializer.data, status=status.HTTP_200_OK)


# to view the cart items
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_cart(request, *args, **kwargs):
    cart = models.Cart.objects.filter(user=request.user).first()
    if cart:
        serializer = serializers.CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"detail": "Cart does not exist."}, status=status.HTTP_404_NOT_FOUND)


# to delete cart item
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_cart_item(request, pk, *args, **kwargs):
    try:
        cart_item = models.CartItem.objects.get(pk=pk, cart__user=request.user)
    except models.CartItem.DoesNotExist:
        return Response({"detail": "Cart item not found."}, status=status.HTTP_404_NOT_FOUND)

    cart_item.delete()
    return Response({"detail": "Cart item deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


# to delete the cart
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_cart(request, *args, **kwargs):
    cart = models.Cart.objects.filter(user=request.user).first()
    if cart:
        cart.delete()
        return Response({"detail": "Cart deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    return Response({"detail": "Cart does not exist."}, status=status.HTTP_404_NOT_FOUND)


# to place the order
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def place_order(request, *args, **kwargs):
    user = request.user
    cart_id = request.data.get('cart_id')
    order_type = request.data.get('order_type')
    coupon_code = request.data.get('coupon_code')

    # check the cart exits
    try:
        cart = models.Cart.objects.get(id=cart_id, user=user)
    except models.Cart.DoesNotExist:
        return Response({"detail": "Cart does not exist."}, status=status.HTTP_404_NOT_FOUND)

    # calculate the total price
    total_price = sum(item.menu_item.price * item.quantity for item in cart.cartitem_set.all())

    # apply the coupon code and calculate the discount
    discount_applied = 0
    coupon = None
    if coupon_code:
        try:
            coupon = models.Coupon.objects.get(code=coupon_code)
            discount_applied = (total_price * coupon.discount_percentage) / 100
        except models.Coupon.DoesNotExist:
            return Response({"detail": "Invalid coupon code."}, status=status.HTTP_404_NOT_FOUND)

    final_price = total_price - discount_applied

    # create a new order
    order = models.Order.objects.create(
        customer=user,
        branch=cart.branch,
        order_type=order_type,
        total_price=total_price,
        discount_applied=discount_applied,
        final_price=final_price,
        coupon=coupon
    )

    # adding cart items to order items table and delete the cart
    cart_items = models.CartItem.objects.filter(cart=cart)
    for cart_item in cart_items:
        models.OrderItem.objects.create(
            order=order,
            menu_item=cart_item.menu_item,
            quantity=cart_item.quantity,
        )
    cart.delete()

    serializer = serializers.OrderSerializer(order)
    return Response({"detail": "Order placed successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)


# to view the places orders by admins according to branch
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_placed_orders(request, branch_id, pk=None, *args, **kwargs):
    user = request.user
    user_type = getattr(user, 'user_type')
    user_branch = getattr(user, 'branch')

    if user_type in ['customer', 'delivery_partner']:
        return Response({"detail: You do not have permission to perform this actions."},
                        status=status.HTTP_403_FORBIDDEN)

    if user_type in ['manger', 'staff'] and branch_id != user_branch.id:
        return Response({"detail: You do not have permission to perform this actions."},
                        status=status.HTTP_403_FORBIDDEN)

    if pk:
        try:
            order = models.Order.objects.get(pk=pk, branch=branch_id)
            serializer = serializers.OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except models.Order.DoesNotExist:
            return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

    orders = models.Order.objects.filter(branch=branch_id)

    if not orders.exists():
        return Response({"detail": "No orders found for this branch."}, status=status.HTTP_404_NOT_FOUND)

    serializer = serializers.OrderSerializer(orders, many=True)

    return Response({"orders": serializer.data}, status=status.HTTP_200_OK)


# to view the order history by user
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_the_order_history(request, pk=None, *args, **kwargs):
    user = request.user
    user_type = getattr(user, 'user_type')

    if user_type != "customer":
        return Response({"detail: You do not have permission to perform this actions."},
                        status=status.HTTP_403_FORBIDDEN)

    if pk:
        try:
            order = models.Order.objects.get(pk=pk)
            serializer = serializers.OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except models.Order.DoesNotExist:
            return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

    orders = models.Order.objects.filter(customer=user)
    serializer = serializers.OrderSerializer(orders, many=True)
    return Response({"orders": serializer.data}, status=status.HTTP_200_OK)
