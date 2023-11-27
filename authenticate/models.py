from django.db import models
from django.contrib.auth.models import User


class SalesCategory(models.Model):
    type = models.CharField(max_length=50)
    def __str__(self):
        return self.type

    def delete(self, *args, **kwargs):
        print(f"Deleting SalesCategory: {self.id}")
        super().delete(*args, **kwargs)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_profile")
    full_name = models.CharField(max_length=264, blank=True)
    job_title = models.CharField(max_length=264, blank=True)
    head_of_sales = models.ForeignKey(User, on_delete=models.CASCADE, related_name="head_of_sales", blank=True, null=True)
    pin = models.IntegerField(null=False, blank=False)
    role_choices = (
            ("CEO", "Management"),
            ("HOS", "Sales Manager"),
            ("Salesperson", "Salesperson"),

    )

    role_type = models.CharField(max_length=265, choices=role_choices, blank=True)
    profile_picture = models.ImageField(upload_to='profile_picture/', blank=True, null=True)
    def __str__(self):
         return self.user.username