from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from . import models
from . import serializers
from django.core.files.uploadedfile import InMemoryUploadedFile
from firebase_config import bucket


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

    # handle image uploads if provided
    image_files = request.FILES.getlist('images')
    branch_images = []

    for image in image_files:
        if not isinstance(image, InMemoryUploadedFile):
            return Response({"detail": "Uploaded file is not in the correct format."}, status=status.HTTP_400_BAD_REQUEST)

        # create a blob for Firebase Storage
        blob = bucket.blob(f'branch_images/{image.name}')
        blob.upload_from_file(image, content_type=image.content_type)
        blob.make_public()
        image_url = blob.public_url

        # create branch instance
        branch_image = models.BranchImage(image_url=image_url)
        branch_images.append(branch_image)

    # prepare data for Branch model
    branch = models.Branch(
        name=request.data.get('name'),
        address=request.data.get('address'),
        contact_number=request.data.get('contact_number'),
        longitude=request.data.get('longitude'),
        latitude=request.data.get('latitude')
    )
    branch.save()

    # save BranchImage instances with the newly created branch
    for branch_image in branch_images:
        branch_image.branch = branch
        branch_image.save()

    serializer = serializers.BranchSerializer(branch)

    return Response({"detail": "Branch created successfully.", "branch": serializer.data}, status=status.HTTP_201_CREATED)


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


# to add images to the branch
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_images_to_branch(request, branch_id, *args, **kwargs):
    user = request.user
    user_type = getattr(user, 'user_type')
    user_branch = getattr(user, 'branch')

    if user_type not in ['admin', 'manager']:
        return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

    try:
        branch = models.Branch.objects.get(pk=branch_id)
    except models.Branch.DoesNotExist:
        return Response({"detail": "Branch not found."}, status=status.HTTP_404_NOT_FOUND)

    if user_type == 'manager' and branch.pk != user_branch.pk:
        return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

    image_files = request.FILES.getlist('images')
    if not image_files:
        return Response({"detail": "No images provided."}, status=status.HTTP_400_BAD_REQUEST)

    branch_images = []

    for image in image_files:
        if not isinstance(image, InMemoryUploadedFile):
            return Response({"detail": "Uploaded file is not in the correct format."}, status=status.HTTP_400_BAD_REQUEST)

        blob = bucket.blob(f'branch_images/{image.name}')
        blob.upload_from_file(image, content_type=image.content_type)
        blob.make_public()
        image_url = blob.public_url

        branch_image = models.BranchImage(branch=branch, image_url=image_url)
        branch_images.append(branch_image)

    models.BranchImage.objects.bulk_create(branch_images)

    serializer = serializers.BranchSerializer(branch)

    return Response({"detail": "Images added successfully.", "branch": serializer.data}, status=status.HTTP_200_OK)


# to delete branch image
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_branch_image(request, image_id, *args, **kwargs):
    user = request.user
    user_type = getattr(user, 'user_type')
    user_branch = getattr(user, 'branch')

    if user_type not in ['admin', 'manager']:
        return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

    try:
        branch_image = models.BranchImage.objects.get(pk=image_id)
    except models.BranchImage.DoesNotExist:
        return Response({"detail": "Image not found."}, status=status.HTTP_404_NOT_FOUND)

    if user_type == "manager" and branch_image.branch.pk != user_branch.pk:
        return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

    # extract the file name from the image url
    image_url = branch_image.image_url
    filename = image_url.split('/')[-1]

    # delete the image from the firebase
    blob = bucket.blob(f'branch_images/{filename}')
    if blob.exists():
        blob.delete()

    # delete the branch image from the database
    branch_image.delete()
    return Response({"detail": "Branch image deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


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

        # getting the images related to the branch
        branch_images = models.BranchImage.objects.filter(branch=branch_data)

        for branch_image in branch_images:
            image_url = branch_image.image_url
            filename = image_url.split('/')[-1]

            blob = bucket.blob(f'branch_images/{filename}')
            if blob.exists():
                blob.delete()

            branch_image.delete()
            
        branch_data.delete()
        return Response({"detail": "Branch deleted successfully."}, status=status.HTTP_200_OK)

    except models.Branch.DoesNotExist:
        return Response({"detail": "Branch not found."}, status=status.HTTP_404_NOT_FOUND)