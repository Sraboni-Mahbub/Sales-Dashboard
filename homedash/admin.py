from django.contrib import admin
from django.contrib.auth.models import User
from homedash.models import *


class ProductsAdmin(admin.ModelAdmin):
    list_display = ('id','p_name', 'sales_category', 'price')

class SalesAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'product_ids', 'product_names', 'sale_value', 'remarks', 'date')
    list_filter = ('user_profile', 'date')
    search_fields = ('user_profile__user__username', 'product__p_name','product__id')

    def product_ids(self, obj):
        return ', '.join([str(product.id) for product in obj.product.all()])

    def product_names(self, obj):
        return ', '.join([product.p_name for product in obj.product.all()])

    product_ids.short_description = 'Product IDs'
    product_names.short_description = 'Product Names'
class LogTableAdmin(admin.ModelAdmin):
    list_display = ('user', 'actions', 'results', 'dateTime', 'description')

class InfoTableAdmin(admin.ModelAdmin):
    list_display = ('fiscal_year', 'month', 'budget')


admin.site.register(Products, ProductsAdmin)
admin.site.register(Sale, SalesAdmin)
admin.site.register(LogTable, LogTableAdmin)
admin.site.register(InfoTable, InfoTableAdmin)

