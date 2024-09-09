from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('create/staff/', views.create_staff, name='create_staff'),
    path('create/user/', views.register_user, name='register_user'),

    path('delete/user/<int:pk>/', views.delete_user, name='delete_user'),
    path('delete/account/', views.delete_customer_account, name='delete_customer_account'),

    path('update/user/<int:pk>/', views.edit_customer_account, name='edit_customer_account'),
    path('update/user/admin/<int:pk>/', views.edit_user_accounts_by_admins, name='edit_user_accounts_by_admins'),
    path('update/account/', views.edit_own_account, name='edit_own_account'),

    path('get/account/', views.get_user_account, name='get_user_account'),
    path('get/account/<int:pk>/', views.get_user_account, name='get_user_account_by_id'),

    path('get/staff/branch/', views.get_staff_by_branch, name='get_staff_by_branch'),
    path('get/staff/branch/<int:pk>/', views.get_staff_by_branch, name='get_staff_by_branch_id')
]
