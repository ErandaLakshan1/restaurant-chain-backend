from django.contrib import admin
from .models import Branch, BranchImage

# Register your models here.
admin.site.register(Branch)
admin.site.register(BranchImage)