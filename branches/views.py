from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from . import models
from . import serializers


# Create your views here.
# to get the branches list
@api_view(['GET'])
def get_branches(request, pk=None, *args, **kwargs):
    if pk:
        try:
            # Retrieve the specific branch
            branch = models.Branch.objects.get(pk=pk)
            serializer = serializers.BranchSerializer(branch)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except models.Branch.DoesNotExist:
            return Response({"detail": "Branch not found."}, status=status.HTTP_404_NOT_FOUND)

    branches = models.Branch.objects.all()
    serializer = serializers.BranchSerializer(branches, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# to add a branch
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_branch(request, *args, **kwargs):
    user = request.user
    user_type = getattr(user, 'user_type')

    if user_type != 'admin':
        return Response({"detail": "You do not have permission to perform this action."},
                        status=status.HTTP_403_FORBIDDEN)

    serializer = serializers.BranchSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({"detail": "Branch created successfully."}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# to update branch
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_branch(request, pk, *args, **kwargs):
    user = request.user
    user_type = getattr(user, 'user_type')

    if user_type != 'admin':
        return Response({"detail": "You do not have permission to perform this action."},
                        status=status.HTTP_403_FORBIDDEN)

    try:
        branch_data = models.Branch.objects.get(pk=pk)
        serializer = serializers.BranchSerializer(branch_data, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Branch updated successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except models.Branch.DoesNotExist:
        return Response({"detail": "Branch not found."}, status=status.HTTP_404_NOT_FOUND)


# to delete branch
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_branch(request, pk, *args, **kwargs):
    user = request.user
    user_type = getattr(user, 'user_type')

    if user_type != 'admin':
        return Response({"detail": "You do not have permission to perform this action."},
                        status=status.HTTP_403_FORBIDDEN)

    try:
        branch_data = models.Branch.objects.get(pk=pk)
        branch_data.delete()
        return Response({"detail": "Branch deleted successfully."}, status=status.HTTP_200_OK)

    except models.Branch.DoesNotExist:
        return Response({"detail": "Branch not found."}, status=status.HTTP_404_NOT_FOUND)