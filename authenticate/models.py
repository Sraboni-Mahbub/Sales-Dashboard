from django.db import models
from django.contrib.auth.models import User


class SalesCategory(models.Model):
    type = models.CharField(max_length=50)
    def __str__(self):
        return self.type

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_profile")
    full_name = models.CharField(max_length=264, blank=True)
    job_title = models.CharField(max_length=264, blank=True)
    head_of_sales = models.ForeignKey(User, on_delete=models.CASCADE, related_name="head_of_sales", blank=True, null=True)
    pin = models.IntegerField(null=False, blank=False)
    role_choices = (
            ("CEO", "CEO"),
            ("HOS", "Head of Sales"),
            ("Salesperson", "Salesperson"),

    )

    role_type = models.CharField(max_length=265, choices=role_choices, blank=True)

    sales_category = models.ForeignKey(SalesCategory, on_delete=models.SET_NULL, related_name="sales_category",
                                       blank=True, null=True)

    def __str__(self):
         return self.user.username





