from django.db import models
from branches.models import Branch
from users.models import CustomUser


# Create your models here.
class Table(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    table_number = models.IntegerField()
    seating_capacity = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return f"{self.table_number} - {self.branch.name}"


class Reservation(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    reservation_date = models.DateField()

    def __str__(self):
        return f"{self.customer.username} - {self.table} - {self.reservation_date}"
