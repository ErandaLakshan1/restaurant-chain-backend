from django.db import models
from users.models import CustomUser
from branches.models import Branch
from menu.models import Menu
import datetime


# Create your models here.
class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    expiration_date = models.DateField()

    def __str__(self):
        return self.code


class Order(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='customer_orders')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    delivery_partner = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True,
                                         related_name='delivery_partner_orders')
    order_type = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    items = models.ManyToManyField(Menu)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_applied = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    final_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.customer.username}"

    def apply_coupon(self):
        if self.coupon and self.coupon.expiration_date >= datetime.date.today():
            self.discount_applied = (self.total_price * self.coupon.discount_percentage) / 100
            self.final_price = self.total_price - self.discount_applied
        else:
            self.final_price = self.total_price

    def save(self, *args, **kwargs):
        self.apply_coupon()
        super().save(*args, **kwargs)
