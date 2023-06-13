from django.contrib import admin
from order.models import Order,OrderItem

class OrderModelAdmin(admin.ModelAdmin):
    list_display = ('shop','total_price', 'order_status')
    search_fields = ('shop__shop_name',)
    list_filter = ('order_status',)

class OrderItemModelAdmin(admin.ModelAdmin):
    list_display = ('order','product','quantity', 'price')
    # search_fields = ('shop__shop_name',)
    # list_filter = ('order_status',)

admin.site.register(Order,OrderModelAdmin)
admin.site.register(OrderItem,OrderItemModelAdmin)
