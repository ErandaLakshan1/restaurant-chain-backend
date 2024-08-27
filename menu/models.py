from django.db import models
from branches.models import Branch


# Create your models here.
class Menu(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=False)
    category = models.CharField(max_length=120)

    def __str__(self):
        return self.name


class MenuImage(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    image_url = models.URLField()

    def __str__(self):
        return f"Image for {self.menu.name} - {self.image_url}"
