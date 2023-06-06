from django.contrib import admin
from connection.models import Connection


class ConnectionModelAdmin(admin.ModelAdmin):
    list_display = ('source_shop','target_shop','status')
    search_fields = ('source_shop__shop_name','target_shop__shop_name')
    list_filter = ('status',)


admin.site.register(Connection,ConnectionModelAdmin)