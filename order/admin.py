from django.contrib import admin
from order.models import Order,OrderItem

class OrderModelAdmin(admin.ModelAdmin):
    list_display = ('organization','total_price', 'order_status')
    search_fields = ('organization.organization_name',)
    list_filter = ('order_status',)

class OrderItemModelAdmin(admin.ModelAdmin):
    list_display = ('order','product','quantity', 'price')

admin.site.register(Order,OrderModelAdmin)
admin.site.register(OrderItem,OrderItemModelAdmin)
