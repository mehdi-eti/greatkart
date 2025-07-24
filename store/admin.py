from django.contrib import admin

from .models import Products, Veriation
# Register your models here.


class ProductsAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock',
                    'category', 'modified_date')
    prepopulated_fields = {'slug': ('product_name',)}

class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'veriation_category',
                    'variation_value', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('veriation_category',
                   'variation_value', 'is_active')


admin.site.register(Products, ProductsAdmin)
admin.site.register(Veriation, VariationAdmin)
