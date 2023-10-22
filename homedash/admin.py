from django.contrib import admin
from django.contrib.auth.models import User
from homedash.models import *


class ProductsAdmin(admin.ModelAdmin):
    list_display = ('id','p_name', 'sales_category', 'price')

class SalesAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'product_ids', 'sale_value', 'date', 'remarks')
    list_filter = ('user_profile', 'date')
    search_fields = ('user_profile__user__username', 'product__p_name')

    def product_ids(self, obj):
        return ', '.join([str(product.id) for product in obj.product.all()])

    product_ids.short_description = 'Product IDs'
class LogTableAdmin(admin.ModelAdmin):
    list_display = ('user', 'actions', 'results', 'dateTime', 'description')


admin.site.register(Products, ProductsAdmin)
admin.site.register(Sale, SalesAdmin)
admin.site.register(LogTable, LogTableAdmin)

