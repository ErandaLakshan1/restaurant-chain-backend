from django.contrib.auth.models import AbstractUser
from django.db import models


# for override the user model
class CustomUser(AbstractUser):
    # Adding custom fields
    user_type = models.CharField(max_length=50, default='user')
    mobile_number = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    nic = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(unique=True)






