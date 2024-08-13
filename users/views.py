from django.shortcuts import render
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
# from models import CustomUser
from . import serializers


# for customize the tokens
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        token['user_type'] = user.user_type
        token['branch'] = user.branch
        token['name'] = user.first_name + ' ' + user.last_name

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# for create a branch manager
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_branch_manger(request, *args, **kwargs):
    user = request.user
    # get user_type from the authenticated user
    user_type = getattr(user, 'user_type')

    if user_type != 'admin':
        return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

    serializer = serializers.CustomUserSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# for create staff and delivery partner
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_staff_and_delivery_partner(request, *args, **kwargs):
    user = request.user
    user_type = getattr(user, 'user_type')

    print(user_type)

    if user_type not in ['admin', 'manager']:
        return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

    serializer = serializers.CustomUserSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# for register user
@api_view(['POST'])
def create_user(request, *args, **kwargs):
    serializer = serializers.CustomUserSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




