from django.contrib import admin
from shop.models import Shop

class ShopModelAdmin(admin.ModelAdmin):
    list_display = ('organization_name','merchant','category', 'active_code','is_active')
    search_fields = ('organization_name',)
    list_filter = ('category__category_name',)




admin.site.register(Shop,ShopModelAdmin)
