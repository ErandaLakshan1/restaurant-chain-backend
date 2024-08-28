from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from . import models
from . import serializers
from branches.models import Branch


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
