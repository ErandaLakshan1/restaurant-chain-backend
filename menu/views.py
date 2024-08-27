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
            return Response({"detail": "Uploaded file is not in the correct format."}, status=status.HTTP_400_BAD_REQUEST)

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


