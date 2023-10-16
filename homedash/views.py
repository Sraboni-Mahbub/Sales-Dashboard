from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required

from authenticate import models
from authenticate.models import *
from homedash.models import *


@login_required(login_url='/authenticate/login/')
def home(request):
    return render(request, 'homedash/index.html')


@login_required(login_url='/authenticate/login/')
def sales_category(request):

    if request.user.user_profile.role_type == 'HOS':
        add_category = SalesCategory.objects.all()
        sales_category = SalesCategory.objects.annotate(product_count=models.Count('sales_category_products'))

        if request.method == 'POST':
            # add_category.type = request.POST.get('type')
            # add_category.save()
            sales_type = request.POST.get('type')
            SalesCategory.objects.create(type=sales_type)
            return redirect('sales_category')


    return render(request, 'homedash/sales_category.html', {'sales_category': sales_category, 'add_category':add_category})


@login_required(login_url='/authenticate/login/')
def view_category(request, category_id):
    sales_category = SalesCategory.objects.get(pk=category_id)
    products = Products.objects.filter(sales_category=sales_category)

    if request.method == 'POST':
        dict = {
            'p_name' : request.POST.get('p_name'),
            'price' : request.POST.get('price'),
        }
        Products.objects.create(**dict, sales_category=sales_category)
        return redirect('view_category', category_id=category_id)

    return render(request, 'homedash/view_category.html', {'sales_category': sales_category, 'products': products})

