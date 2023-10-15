from django.db import models
from django.contrib.auth.models import User
from authenticate.models import UserProfile, SalesCategory



class Products(models.Model):
    sales_category = models.ForeignKey(SalesCategory, on_delete=models.CASCADE,  related_name="sales_category_products",
                                       blank=True, null=True)
    p_name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.p_name

class Sale(models.Model):
    product = models.ManyToManyField(Products)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    sale_value = models.DecimalField(max_digits=10, decimal_places=2)
    remarks = models.CharField(max_length=50)
    date = models.DateTimeField()

    def __str__(self):
        product_names = ', '.join([product.p_name for product in self.product.all()])
        return f"{product_names}"

class LogTable(models.Model):
    user = models.CharField(max_length=50)
    actions = models.CharField(max_length=50)
    results = models.CharField(max_length=50)
    dateTime = models.DateTimeField()
    description = models.CharField(max_length=50)

    def __str__(self):
        return self.user

