from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
        path('', views.home, name='index'),
        path('sales_category', views.sales_category, name='sales_category'),
        path('view_category/<int:category_id>', views.view_category, name='view_category'),
        path('view_user_category/<int:category_id>/', views.view_user_category, name='view_user_category'),
        path('add_sale/', views.add_sale, name='add_sale'),
]