from django.db import models


# Create your models here.
class Branch(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=20)
    longitude = models.FloatField()
    latitude = models.FloatField()

    def __str__(self):
        return self.name


class BranchImage(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    image_url = models.URLField()

    def __str__(self):
        return f"Image for {self.branch.name} - {self.image_url}"
