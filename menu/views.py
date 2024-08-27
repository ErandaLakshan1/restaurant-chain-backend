from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from . import models
from . import serializers
from django.core.files.uploadedfile import InMemoryUploadedFile
from firebase_config import bucket


# Create your views here.
# to add menu items
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_menu(request, *args, **kwargs):
    user = request.user
    user_type = getattr(user, 'user_type')
    user_branch = getattr(user, 'branch')

    if user_type in ['customer', 'delivery_partner']:
        return Response({"detail: You do not have permission to perform this actions."},
                        status=status.HTTP_403_FORBIDDEN)

    # handle image upload
    image_files = request.FILES.getlist('images')
    menu_images = []

    for image in image_files:
        if not isinstance(image, InMemoryUploadedFile):
            return Response({"detail": "Uploaded file is not in the correct format."},
                            status=status.HTTP_400_BAD_REQUEST)

        # create a blob for Firebase Storage
        blob = bucket.blob(f'menu_images/{image.name}')
        blob.upload_from_file(image, content_type=image.content_type)
        blob.make_public()
        image_url = blob.public_url

        # create menu instance
        menu_image = models.MenuImage(image_url=image_url)
        menu_images.append(menu_image)

    if user_type == 'admin':
        branch_id = request.data.get('branch')
        if not branch_id:
            return Response({"detail": "Branch ID is required for admin users."},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            branch = models.Branch.objects.get(id=branch_id)
        except models.Branch.DoesNotExist:
            return Response({"detail": "Invalid branch ID."}, status=status.HTTP_400_BAD_REQUEST)
    else:
        branch = user_branch

    # prepare data for menu model
    menu = models.Menu(
        name=request.data.get('name'),
        description=request.data.get('description'),
        price=request.data.get('price'),
        branch=branch,
        is_available=request.data.get('is_available'),
        category=request.data.get('category'),
    )
    menu.save()

    # save menu image instance with the newly created menu item
    for menu_image in menu_images:
        menu_image.menu = menu
        menu_image.save()

    serializer = serializers.MenuSerializer(menu)

    return Response({"detail": "Menu item added successfully.", "menu": serializer.data}, status=status.HTTP_200_OK)


# to get menu items for admins
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_menu_items(request, pk=None, *args, **kwargs):
    user = request.user
    user_type = getattr(user, 'user_type')
    user_branch = getattr(user, 'branch')

    if user_type in ['customer', 'delivery_partner']:
        return Response({"detail: You do not have permission to perform this actions."},
                        status=status.HTTP_403_FORBIDDEN)

    if user_type in ['manager', 'staff']:
        if pk:
            try:
                menu_item = models.Menu.objects.get(pk=pk, branch=user_branch)
                serializer = serializers.MenuSerializer(menu_item)
                return Response(serializer.data, status=status.HTTP_200_OK)

            except models.Menu.DoesNotExist:
                return Response({"detail": "Menu item does not exist."}, status=status.HTTP_404_NOT_FOUND)

        menu_items = models.Menu.objects.filter(branch=user_branch)
        serializer = serializers.MenuSerializer(menu_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if pk:
        try:
            menu_item = models.Menu.objects.get(pk=pk)
            serializer = serializers.MenuSerializer(menu_item)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except models.Menu.DoesNotExist:
            return Response({"detail": "Menu item does not exist."}, status=status.HTTP_404_NOT_FOUND)

    menu_items = models.Menu.objects.all()
    serializer = serializers.MenuSerializer(menu_items, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# to get menu items by users according to branch
@api_view(['GET'])
def get_meu_items_according_to_branch(request, branch_id, pk=None, *args, **kwargs):
    if pk:
        try:
            menu_item = models.Menu.objects.get(pk=pk, branch=branch_id)
            serializer = serializers.MenuSerializer(menu_item)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except models.Menu.DoesNotExist:
            return Response({"detail": "Menu item does not exist."}, status=status.HTTP_404_NOT_FOUND)

    menu_items = models.Menu.objects.filter(branch=branch_id)
    serializer = serializers.MenuSerializer(menu_items, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# to update menu items
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_menu_item(request, pk, *args, **kwargs):
    user = request.user
    user_type = getattr(user, 'user_type')
    user_branch = getattr(user, 'branch')

    if user_type in ['customer', 'delivery_partner']:
        return Response({"detail: You do not have permission to perform this actions."},
                        status=status.HTTP_403_FORBIDDEN)

    try:
        menu_item = models.Menu.objects.get(pk=pk)

    except models.Menu.DoesNotExist:
        return Response({"detail": "Menu item does not exist."}, status=status.HTTP_404_NOT_FOUND)

    if user_type in ['manager', 'staff']:
        if menu_item.branch != user_branch:
            return Response({"detail": "You do not have permission to update this menu item."},
                            status=status.HTTP_403_FORBIDDEN)

    serializer = serializers.MenuSerializer(menu_item, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"detail": "Menu item updated successfully."}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# to delete menu item images
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_menu_item_images(request, pk, *args, **kwargs):
    user = request.user
    user_type = getattr(user, 'user_type')
    user_branch = getattr(user, 'branch')

    if user_type in ['customer', 'delivery_partner']:
        return Response({"detail: You do not have permission to perform this actions."},
                        status=status.HTTP_403_FORBIDDEN)

    try:
        menu_item_image = models.MenuImage.objects.get(pk=pk)
    except models.MenuImage.DoesNotExist:
        return Response({"detail": "Menu item image does not exist."}, status=status.HTTP_404_NOT_FOUND)

    menu_item = menu_item_image.menu

    if user_type in ['manager', 'staff'] and menu_item.branch != user_branch:
        return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

    # extract the file name from the image url
    image_url = menu_item_image.image_url
    file_name = image_url.split('/')[-1]

    # delete the image form firebase
    blob = bucket.blob(f'menu_images/{file_name}')
    if blob.exists():
        blob.delete()

    # delete the branch image form the database
    menu_item_image.delete()
    return Response({"detail": "Menu item image deleted successfully."}, status=status.HTTP_200_OK)


# to add images to menu items
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_images_to_menu_item(request, pk, *args, **kwargs):
    user = request.user
    user_type = getattr(user, 'user_type')
    user_branch = getattr(user, 'branch')

    if user_type in ['customer', 'delivery_partner']:
        return Response({"detail: You do not have permission to perform this actions."},
                        status=status.HTTP_403_FORBIDDEN)

    try:
        menu_item = models.Menu.objects.get(pk=pk)
    except models.Menu.DoesNotExist:
        return Response({"detail": "Menu item does not exist."}, status=status.HTTP_404_NOT_FOUND)

    if user_type in ['manager', 'staff'] and menu_item.branch != user_branch:
        return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

    image_files = request.FILES.getlist('images')

    if not image_files:
        return Response({"detail": "No images provided."}, status=status.HTTP_400_BAD_REQUEST)

    menu_item_images = []

    for image in image_files:
        if not isinstance(image, InMemoryUploadedFile):
            return Response({"detail": "Uploaded file is not in the correct format."}, status=status.HTTP_400_BAD_REQUEST)

        blob = bucket.blob(f'menu_images/{image.name}')
        blob.upload_from_file(image, content_type=image.content_type)
        blob.make_public()
        image_url = blob.public_url

        menu_item_image = models.MenuImage(menu=menu_item, image_url=image_url)
        menu_item_images.append(menu_item_image)

    models.MenuImage.objects.bulk_create(menu_item_images)
    return Response({"detail": "Images added successfully."}, status=status.HTTP_200_OK)
