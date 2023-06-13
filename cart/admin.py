from django.contrib import admin
from cart.models import Cart,CartItem

class CartModelAdmin(admin.ModelAdmin):
    list_display = ('shop',)
    search_fields = ('shop__shop_name',)
    list_filter = ('shop__shop_name',)


class CartItemModelAdmin(admin.ModelAdmin):
    list_display = ('cart','product','quantity','price')
    search_fields = ('product',)


admin.site.register(Cart,CartModelAdmin)
admin.site.register(CartItem,CartItemModelAdmin)