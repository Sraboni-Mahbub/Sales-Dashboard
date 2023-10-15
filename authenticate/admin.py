from django.contrib import admin
from django.contrib.auth.models import User
from authenticate.models import UserProfile, SalesCategory

class UserProfileAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'head_of_sales':
            # Filter the choices for 'head_of_sales' based on 'role_type'
            kwargs['queryset'] = User.objects.filter(user_profile__role_type='HOS')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    list_display = ('user', 'full_name', 'job_title', 'role_type')

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(SalesCategory)
