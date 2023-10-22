from datetime import timezone
from django.db.models import Q

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from datetime import datetime
from authenticate import models
from authenticate.models import *
from homedash.models import *


@login_required(login_url='/authenticate/login/')
def home(request):
    return render(request, 'homedash/index.html')


@login_required(login_url='/authenticate/login/')
def sales_category(request):

    if request.user.user_profile.role_type == 'HOS' or request.user.user_profile.role_type == 'CEO':
        add_category = SalesCategory.objects.all()
        sales_category = SalesCategory.objects.annotate(product_count=models.Count('sales_category_products'))


        if request.method == 'POST':
            sales_type = request.POST.get('type')
            SalesCategory.objects.create(type=sales_type)
            return redirect('sales_category')


    return render(request, 'homedash/sales_category.html',
                  {'sales_category': sales_category,
                   'add_category':add_category,})


#Adding products here too
@login_required(login_url='/authenticate/login/')
def view_category(request, category_id):
    sales_category = SalesCategory.objects.get(pk=category_id)
    products = Products.objects.filter(sales_category=sales_category)

    if request.method == 'POST':
        dict = {
            'p_name' : request.POST.get('p_name'),
            'price' : request.POST.get('price'),
        }
        new_product = Products.objects.create(**dict, sales_category=sales_category)
        return redirect('view_category', category_id=new_product.sales_category.pk)

    return render(request, 'homedash/view_category.html', {'sales_category': sales_category, 'products': products})


@login_required(login_url='/authenticate/login/')
def view_user_category(request, category_id):
    sales_category = SalesCategory.objects.get(pk=category_id)

    user_profiles = UserProfile.objects.filter(sales_category=sales_category)

    context = {
        'sales_category': sales_category,
        'user_profiles': user_profiles,
    }

    return render(request, 'homedash/view_user_category.html', context)

def add_sale(request):
    if request.method == 'POST':

        product_ids = request.POST.getlist('product')
        username = request.POST.get('username')
        sale_value = request.POST.get('sale_value')
        remarks = request.POST.get('remarks')


        products = Products.objects.filter(id__in=product_ids)
        user_profile = UserProfile.objects.get(user__username=username)


        product_id_list = [str(product.id) for product in products]


        new_sale = Sale.objects.create(
            user_profile=user_profile,
            sale_value=sale_value,
            remarks=remarks,
            date=datetime.now()
        )

        new_sale.product.set(products)

        return redirect('add_sale')

    else:
        products = Products.objects.all()
        user_profiles = UserProfile.objects.all()

    return render(request, 'homedash/add_sale.html', {'products': products, 'user_profiles': user_profiles})

def search(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        product_id = request.GET.get('product_id')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')

        query = Q()

        if username:
            query &= Q(user_profile__user__username=username)
        if product_id:
            query &= Q(product__id=product_id)
        if start_date and end_date:
            query &= Q(date__range=[start_date, end_date])
        if min_price:
            query &= Q(sale_value__gte=min_price)
        if max_price:
            query &= Q(sale_value__lte=max_price)

        results = Sale.objects.filter(query)

    return render(request, 'homedash/search.html', {'results': results})

