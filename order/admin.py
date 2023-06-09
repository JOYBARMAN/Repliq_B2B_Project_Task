from django.contrib import admin
from order.models import Order

class OrderModelAdmin(admin.ModelAdmin):
    list_display = ('shop','product','total_price', 'order_status')
    search_fields = ('shop__shop_name',)
    list_filter = ('order_status',)


admin.site.register(Order,OrderModelAdmin)
