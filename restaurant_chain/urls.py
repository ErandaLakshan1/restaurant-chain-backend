"""
URL configuration for restaurant_chain project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # for users
    path('api/users/', include('users.urls')),
    # for branches
    path('api/branches/', include('branches.urls')),
    # for menu
    path('api/menu/', include('menu.urls')),
    # for reservations
    path('api/reservation/', include('reservation.urls')),
    # for orders
    path('api/orders/', include('orders.urls'))
]
