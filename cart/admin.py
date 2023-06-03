from django.contrib import admin
from cart.models import Cart,CartItem

class CartModelAdmin(admin.ModelAdmin):
    list_display = ('shop','total', 'is_complete')
    search_fields = ('shop',)
    list_filter = ('is_complete',)

class CartItemModelAdmin(admin.ModelAdmin):
    list_display = ('cart', 'sub_total')
    # search_fields = ('product_name',)
    # list_filter = ('price','shop__category')

admin.site.register(Cart,CartModelAdmin)
admin.site.register(CartItem,CartItemModelAdmin)
