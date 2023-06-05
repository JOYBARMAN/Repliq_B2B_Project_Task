from django.db import models
from shop.models import Shop
import uuid

class Product(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    shop = models.ForeignKey(Shop,on_delete=models.CASCADE)
    product_name=models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    description=models.TextField()
    image = models.ImageField(upload_to="product/images/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_name

