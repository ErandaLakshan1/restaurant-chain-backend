from django.shortcuts import render
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from . import models
from . import serializers
from django.core.mail import send_mail
from django.conf import settings
import random
import string


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
        token['branch'] = user.branch.pk if user.branch else None
        token['name'] = user.first_name + ' ' + user.last_name

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# for create a branch manager staff and delivery partner
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_staff(request, *args, **kwargs):
    user = request.user
    user_type = getattr(user, 'user_type')
    user_branch = getattr(user, 'branch')

    if user_type not in ['admin', 'manager']:
        return Response({"detail": "You do not have permission to perform this action."},
                        status=status.HTTP_403_FORBIDDEN)

    if user_type == 'manager' and user_branch.pk != int(request.data['branch']):
        return Response({"detail": "You do not have permission to perform this action."},
                        status=status.HTTP_403_FORBIDDEN)

    # to generate a random password
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))

    data = request.data.copy()
    data['password'] = password

    serializer = serializers.CustomUserSerializer(data=data)

    if serializer.is_valid():
        user = serializer.save()

        # Send email with the password
        send_mail(
            'Your New Account Password',
            f'Your account has been created.\n'
            f'Your username is: {request.data.get("username")}.\n'
            f'Your password is: {password}.\n'
            f'You can change this by navigating to your profile.\nThank you.',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        return Response({"detail": "Account created successfully."}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# for register user
@api_view(['POST'])
def register_user(request, *args, **kwargs):
    serializer = serializers.CustomUserSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({"detail": "Account created successfully."}, status=status.HTTP_201_CREATED)
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

        if (user_type == 'admin' and user_data.branch != '') or (
                user_type == 'manager' and user_data.branch == user_branch):
            user_data.delete()
            return Response({"detail": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

        return Response({"detail": "You do not have permission to perform this action."},
                        status=status.HTTP_403_FORBIDDEN)

    except models.CustomUser.DoesNotExist:
        return Response({"detail": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)


# for delete customer account
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_customer_account(request, *args, **kwargs):
    user = request.user
    user_id = getattr(user, 'id')

    try:
        user_data = models.CustomUser.objects.get(pk=user.pk)

        if user_id == user_data.id:
            user_data.delete()
            return Response({"detail": "your account successfully deleted."}, status=status.HTTP_204_NO_CONTENT)

        return Response({"detail": "You do not have permission to perform this action."},
                        status=status.HTTP_403_FORBIDDEN)

    except models.CustomUser.DoesNotExist:

        return Response({"detail": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)


# for edit customer account by customer
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def edit_customer_account(request, pk, *args, **kwargs):
    user = request.user
    user_id = getattr(user, 'id')

    try:
        user_data = models.CustomUser.objects.get(pk=pk)

        if user_id == user_data.id:
            serializer = serializers.CustomUserSerializer(user_data, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"detail": "Account updated successfully."}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "You do not have permission to perform this action."},
                        status=status.HTTP_403_FORBIDDEN)

    except models.CustomUser.DoesNotExist:

        return Response({"detail": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)


# for edit user accounts by admins
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def edit_user_accounts_by_admins(request, pk, *args, **kwargs):
    current_user = request.user
    user_type = getattr(current_user, 'user_type')
    user_branch = getattr(current_user, 'branch')

    try:
        user_data = models.CustomUser.objects.get(pk=pk)

        if (user_type == 'admin' and user_data.branch != '') or (
                user_type == 'manager' and user_data.branch == user_branch):
            serializer = serializers.CustomUserSerializer(user_data, data=request.data, partial=True)
            if serializer.is_valid():
                validated_data = serializer.validated_data

                # restrict the admins to change the password or the username
                if 'username' in validated_data or 'password' in validated_data:
                    return Response({"detail": "You are not allowed to update the username or password."},
                                    status=status.HTTP_400_BAD_REQUEST)

                if user_type == 'manager' and 'user_type' in validated_data:
                    return Response({"detail": "Your are not allowed to change the user type."},
                                    status=status.HTTP_400_BAD_REQUEST)

                serializer.save()
                return Response({"detail": "Account updated successfully."}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "You do not have permission to perform this action."},
                        status=status.HTTP_403_FORBIDDEN)

    except models.CustomUser.DoesNotExist:
        return Response({"detail": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)


# for edit their own accounts by users
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def edit_own_account(request, *args, **kwargs):
    current_user = request.user
    user_type = getattr(current_user, 'user_type')
    print(user_type)

    try:
        user_data = models.CustomUser.objects.get(pk=current_user.pk)
        serializer = serializers.CustomUserSerializer(user_data, data=request.data, partial=True)

        if serializer.is_valid():
            validated_data = serializer.validated_data

            if user_type == 'admin':

                if 'password' in validated_data:
                    return Response({"detail": "You are not allowed to update the password."},
                                    status=status.HTTP_400_BAD_REQUEST)

            elif user_type == 'delivery_partner' or user_type == 'manager' or user_type == 'staff':

                if 'user_type' in validated_data:
                    return Response({"detail": "You are not allowed to update the user type."},
                                    status=status.HTTP_400_BAD_REQUEST)

                if 'branch' in validated_data:
                    return Response({"detail": "You are not allowed to update the branch."},
                                    status=status.HTTP_400_BAD_REQUEST)

            # Save updated data
            serializer.save()
            return Response({"detail": "Account updated successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except models.CustomUser.DoesNotExist:
        return Response({"detail": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_account(request, pk=None, *args, **kwargs):
    current_user = request.user
    user_type = getattr(current_user, 'user_type')
    user_branch = getattr(current_user, 'branch')

    if pk:

        try:
            user_data = models.CustomUser.objects.get(pk=pk)

            if user_type == 'admin' or user_type == 'manager' and user_data.branch == user_branch:

                if user_data.user_type == "customer":
                    return Response({"detail": "You do not have permission to perform this action."},
                                    status=status.HTTP_403_FORBIDDEN)

                serializer = serializers.CustomUserSerializer(user_data)
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response({"detail": "You do not have permission to perform this action."},
                            status=status.HTTP_403_FORBIDDEN)

        except models.CustomUser.DoesNotExist:
            return Response({"detail": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)

    else:
        user = models.CustomUser.objects.get(pk=current_user.pk)
        serializer = serializers.CustomUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


# to get staff list by the branch
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_staff_by_branch(request, pk=None, *args, **kwargs):
    current_user = request.user
    user_type = getattr(current_user, 'user_type')
    user_branch = getattr(current_user, 'branch')

    if pk:
        if user_type == "admin":

            user_data = models.CustomUser.objects.filter(branch=pk)

            if user_data.exists():
                serializer = serializers.CustomUserSerializer(user_data, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

            else:
                return Response({"detail": "No staff found for this branch."}, status=status.HTTP_404_NOT_FOUND)

        return Response({"detail": "You do not have permission to perform this action."},
                        status=status.HTTP_403_FORBIDDEN)

    else:
        if user_type == "manager":
            user_data = models.CustomUser.objects.filter(branch=user_branch)

            if user_data.exists():
                serializer = serializers.CustomUserSerializer(user_data, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

            else:
                return Response({"detail": "No staff found for this branch."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"detail": "You do not have permission to perform this action."},
                            status=status.HTTP_403_FORBIDDEN)
