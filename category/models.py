from django.db import models
import uuid

class Category(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    category_name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.category_name
    
    class Meta:
        verbose_name = "Shop Category"