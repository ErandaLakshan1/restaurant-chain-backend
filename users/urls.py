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
]