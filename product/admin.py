from django.contrib import admin
from product.models import Product


class ProductModelAdmin(admin.ModelAdmin):
    list_display = ('shop','product_name', 'price')
    search_fields = ('product_name',)
    list_filter = ('price','shop__category')


admin.site.register(Product,ProductModelAdmin)