from django.contrib import admin
from cart.models import Cart

class CartModelAdmin(admin.ModelAdmin):
    list_display = ('shop','product', 'quantity')
    search_fields = ('product__product_name',)
    list_filter = ('shop__shop_name',)


admin.site.register(Cart,CartModelAdmin)
