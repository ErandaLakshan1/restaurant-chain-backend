from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


urlpatterns = [
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('create/branchmanger/', views.create_branch_manger),
    path('create/staff/', views.create_staff_and_delivery_partner),
    path('create/user/', views.create_user),

    path('delete/user/<int:pk>/', views.delete_user),
    path('delete/user_account/', views.delete_customer_account),

    path('update/user/<int:pk>/', views.edit_customer_account),
    path('update/user_accounts_by_admins/<int:pk>/', views.edit_user_accounts_by_admins),
    path('update/user/account/', views.edit_own_account),
]