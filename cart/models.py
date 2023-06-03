from django.db import models
from shop.models import Shop
from product.models import Product
import uuid

class Cart(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    shop = models.ForeignKey(Shop,on_delete=models.CASCADE)
    total = models.PositiveIntegerField()
    is_complete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.shop.shop_name
    

class CartItem(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    product = models.ManyToManyField(Product)
    quantity = models.PositiveIntegerField()
    sub_total = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart
