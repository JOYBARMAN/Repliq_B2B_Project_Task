from django.db import models
from shop.models import Shop


status = (
    ("pending", "pending"),
    ("approved", "approved"),
    ("rejected", "rejected")
)


class Connection(models.Model):
    source_shop = models.ForeignKey(
        Shop, on_delete=models.CASCADE, related_name='sent_connection')
    target_shop = models.ForeignKey(
        Shop, on_delete=models.CASCADE, related_name='received_connection')
    status = models.CharField(
        max_length=100, choices=status, default="pending")

    def __str__(self):
        return self.source_shop.shop_name +" and "+ str(self.target_shop.shop_name )+" status is "+ str(self.status)
