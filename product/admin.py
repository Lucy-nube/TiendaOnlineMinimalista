from django.contrib import admin
from .models import Product, Category

admin.site.register(Category)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']
    list_editable = ['price']
    prepopulated_fields = {'slug': ('name',)}

