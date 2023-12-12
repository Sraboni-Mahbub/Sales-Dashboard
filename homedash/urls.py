from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
        path('', views.home, name='index'),
        path('sales_category', views.sales_category, name='sales_category'),
        path('delete_sales_category/<int:category_id>/', views.delete_sales_category, name='delete_sales_category'),
        path('view_category/<int:category_id>', views.view_category, name='view_category'),
        path('view_user_category/<int:category_id>/', views.view_user_category, name='view_user_category'),
        path('add_sale/', views.add_sale, name='add_sale'),
        path('search/', views.search, name='search'),
        path('add_budget/', views.add_budget, name='add_budget'),
        path('update_sale/<int:sale_id>/', views.update_sale, name='update_sale'),
]