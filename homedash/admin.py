from django.contrib import admin
from django.contrib.auth.models import User
from homedash.models import *


class ProductsAdmin(admin.ModelAdmin):
    list_display = ('id','p_name', 'sales_category', 'price')

class SalesAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'product_id', 'product_name', 'sale_value', 'remarks', 'date')
    list_filter = ('user_profile', 'date')
    search_fields = ('user_profile__user__username', 'product__p_name', 'product__id')

    def product_id(self, obj):
        return obj.product.id if obj.product else None

    def product_name(self, obj):
        return obj.product.p_name if obj.product else None

    product_id.short_description = 'Product ID'
    product_name.short_description = 'Product Name'
class LogTableAdmin(admin.ModelAdmin):
    list_display = ('user', 'actions', 'results', 'dateTime', 'description')

class InfoTableAdmin(admin.ModelAdmin):
    list_display = ('fiscal_year', 'month', 'budget')


admin.site.register(Products, ProductsAdmin)
admin.site.register(Sale, SalesAdmin)
admin.site.register(LogTable, LogTableAdmin)
admin.site.register(InfoTable, InfoTableAdmin)

