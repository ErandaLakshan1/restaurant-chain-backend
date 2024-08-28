from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from . import models
from . import serializers
from branches.models import Branch


# Create your views here.
# to get the table list according to branch and get the table data
@api_view(['GET'])
def get_table_list(request, branch_id, pk=None, *args, **kwargs):
    try:
        Branch.objects.get(id=branch_id)
    except Branch.DoesNotExist:
        return Response({"detail": "Invalid branch ID."}, status=status.HTTP_400_BAD_REQUEST)

    if pk:
        try:
            table = models.Table.objects.get(pk=pk, branch_id=branch_id)
            serializer = serializers.TableSerializer(table)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except models.Table.DoesNotExist:
            return Response({"detail": "Table not found."}, status=status.HTTP_404_NOT_FOUND)

    tables = models.Table.objects.filter(branch=branch_id)
    serializer = serializers.TableSerializer(tables, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# to create a table
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_table(request, *args, **kwargs):
    user = request.user
    user_type = getattr(user, 'user_type')
    user_branch = getattr(user, 'branch')

    if user_type in ['customer', 'delivery_partner']:
        return Response({"detail: You do not have permission to perform this actions."},
                        status=status.HTTP_403_FORBIDDEN)

    if user_type == 'admin':
        branch_id = request.data.get('branch')

        if not branch_id:
            return Response({"detail": "Branch ID is required for admin users."},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            branch = Branch.objects.get(id=branch_id)
        except Branch.DoesNotExist:
            return Response({"detail": "Invalid branch ID."}, status=status.HTTP_400_BAD_REQUEST)
    else:
        branch = user_branch

    data = request.data.copy()
    data['branch'] = branch.id

    serializer = serializers.TableSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({"detail": "Table created successfully."}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# to update table
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_table_details(request, *args, pk, **kwargs):
    user = request.user
    user_type = getattr(user, 'user_type')
    user_branch = getattr(user, 'branch')

    if user_type in ['customer', 'delivery_partner']:
        return Response({"detail": "You do not have permission to perform this action."},
                        status=status.HTTP_403_FORBIDDEN)

    try:
        table = models.Table.objects.get(pk=pk)
    except models.Table.DoesNotExist:
        return Response({"detail": "Table not found."}, status=status.HTTP_404_NOT_FOUND)

    if user_type in ['manager', 'staff'] and table.branch.id != user_branch:
        return Response({"detail": "You do not have permission to update this table."},
                        status=status.HTTP_403_FORBIDDEN)

    serializer = serializers.TableSerializer(table, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"detail": "Table updated successfully."}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# to delete the table
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_table(request, pk, *args, **kwargs):
    user = request.user
    user_type = getattr(user, 'user_type')
    user_branch = getattr(user, 'branch')

    if user_type in ['customer', 'delivery_partner']:
        return Response({"detail": "You do not have permission to perform this action."},
                        status=status.HTTP_403_FORBIDDEN)

    try:
        table = models.Table.objects.get(pk=pk)
    except models.Table.DoesNotExist:
        return Response({"detail": "Table not found."}, status=status.HTTP_404_NOT_FOUND)

    if user_type in ['manager', 'staff'] and table.branch.id != user_branch:
        return Response({"detail": "You do not have permission to perform this action."},
                        status=status.HTTP_403_FORBIDDEN)

    table.delete()
    return Response({"detail": "Table deleted successfully."}, status=status.HTTP_200_OK)
