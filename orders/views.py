from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from . import models
from . import serializers
from branches.models import Branch
from menu.models import Menu


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