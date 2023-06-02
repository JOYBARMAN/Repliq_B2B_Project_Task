from django.contrib import admin
from category.models import Category

class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ('category_name','description', 'created_at')
    search_fields = ('category_name',)
    ordering = ('created_at',)


admin.site.register(Category,CategoryModelAdmin)