from django.contrib import admin
from django.contrib.auth.models import User
from homedash.models import *


class ProductsAdmin(admin.ModelAdmin):
    list_display = ('id','p_name', 'sales_category', 'price')

class SalesAdmin(admin.ModelAdmin):
    list_display = ('display_product_names', 'user_profile', 'sale_value', 'remarks', 'date')

    def display_product_names(self, obj):
        product_names = ', '.join([product.p_name for product in obj.product.all()])
        return product_names

    display_product_names.short_description = 'Products'

class LogTableAdmin(admin.ModelAdmin):
    list_display = ('user', 'actions', 'results', 'dateTime', 'description')


admin.site.register(Products, ProductsAdmin)
admin.site.register(Sale, SalesAdmin)
admin.site.register(LogTable, LogTableAdmin)

