from django.db import models
from shop.models import Shop
import uuid


class OrderStatus(models.TextChoices):
   PENDING = "PENDING","Pending"
   SHIPPED = "SHIPPED","Shipped"
   DELIVERED = "DELIVERED","Delivered"
   COMPLETED = "COMPLETED","Completed"
   CANCELED = "CANCELED","Canceled"



class Order(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    product = models.TextField()
    total_price = models.PositiveIntegerField()
    order_status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.shop.shop_name
