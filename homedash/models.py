from django.db import models
from django.contrib.auth.models import User
from authenticate.models import UserProfile, SalesCategory

class Products(models.Model):
    sales_category = models.ForeignKey(SalesCategory, on_delete=models.CASCADE, related_name="sales_category_products",
                                       blank=True, null=True)
    p_name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.p_name

class Sale(models.Model):
    product = models.ManyToManyField(Products, related_name="sale_product")
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="user_profile")
    sale_value = models.DecimalField(max_digits=10, decimal_places=2)
    remarks = models.CharField(max_length=50)
    date = models.DateTimeField()

    def __str__(self):
        product_ids = ', '.join([str(product.id) for product in self.product.all()])
        return f"Product IDs: {product_ids}, Sale Value: {self.sale_value}, Remarks: {self.remarks}"

class LogTable(models.Model):
    user = models.CharField(max_length=50)
    actions = models.CharField(max_length=50)
    results = models.CharField(max_length=50)
    dateTime = models.DateTimeField()
    description = models.CharField(max_length=50)

    def __str__(self):
        return self.user


class InfoTable(models.Model):
    fiscal_year = models.PositiveIntegerField()
    month = models.CharField(max_length=10,
            choices=[("January", "January"), ("February", "February"), ("March", "March"),
                     ("April", "April"), ("May", "May"), ("June", "June"),
                     ("July", "July"), ("August", "August"), ("September", "September"),
                     ("October", "October"),("November", "November"), ("December", "December")])
    budget = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.month} {self.fiscal_year}"

