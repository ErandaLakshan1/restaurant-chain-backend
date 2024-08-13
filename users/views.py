from django.shortcuts import render
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from . import models
from . import serializers


# for customize the tokens
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['id'] = user.id
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


# for delete account
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request, pk, *args, **kwargs):
    current_user = request.user
    user_type = getattr(current_user, 'user_type')
    user_branch = getattr(current_user, 'branch')

    try:
        user_data = models.CustomUser.objects.get(pk=pk)

        if user_type == 'admin' and user_data.branch != '':
            user_data.delete()
            return Response({"detail": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

        elif user_type == 'manager' and user_data.branch == user_branch:
            user_data.delete()
            return Response({"detail": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

        else:
            return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

    except models.CustomUser.DoesNotExist:
        return Response({"detail": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)


# for delete user account
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user_account(request, pk, *args, **kwargs):
    user = request.user
    user_id = getattr(user, 'id')

    try:
        user_data = models.CustomUser.objects.get(pk=pk)

        if user_id == user_data.id:
            user_data.delete()
            return Response({"detail": "your account successfully deleted."}, status=status.HTTP_204_NO_CONTENT)

        return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

    except models.CustomUser.DoesNotExist:

        return Response({"detail": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)



