from django.db import models
from account_api.models import User
from category.models import Category
import uuid

class Shop(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    merchant = models.ForeignKey(User,on_delete=models.CASCADE)
    organization_name = models.CharField(max_length=255)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    description = models.TextField()
    active_code = models.CharField(max_length=20)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return self.organization_name