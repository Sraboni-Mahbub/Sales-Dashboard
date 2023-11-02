from datetime import timezone, timedelta
from django.db.models import Q

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from datetime import datetime
from django.db.models import Count
from django.db.models.functions import TruncMonth

from django.db.models import Sum, Avg
import locale
from authenticate import models
from authenticate.models import *
from homedash.models import *

def get_chart_data():
    monthly_sales = Sale.objects.annotate(
        month=TruncMonth('date')
    ).values('month').annotate(
        total_sales=Sum('sale_value')
    ).order_by('month')
    month_list = [ 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    monthly_sales_list = [0]*12
    for data in monthly_sales:
        monthly_sales_list[data['month'].month-1] = (int(data['total_sales']))
    # print(prev_12_month)
    print(monthly_sales_list)
    print(month_list)

    return month_list, monthly_sales_list



@login_required(login_url='/authenticate/login/')
def home(request):
    prev_12_month, monthly_sales_list = get_chart_data()
    # Monthly Revenue
    last_thirty_days = datetime.now()-timedelta(days=30)
    total_sales = Sale.objects.filter(date__gte=last_thirty_days).aggregate(sum_sale=Sum('sale_value'))

    total_sales_value = total_sales['sum_sale'] or 0
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    total_sales_value_formatted = locale.format_string("%d", total_sales_value, grouping=True)

    # Yearly Revenue

    current_year = datetime.now().year
    start_date = datetime(current_year, 1, 1)
    end_date = datetime(current_year, 12, 31)
    total_annual_sales = Sale.objects.filter(date__range=(start_date, end_date)).aggregate(sum_sale=Sum('sale_value'))

    total_annual_sales_value = total_annual_sales['sum_sale'] or 0

    total_annual_sales_formatted = locale.format_string("%d", total_annual_sales_value, grouping=True)

    # Number of sales

    last_thirty_sales= datetime.now()-timedelta(days=30)
    last_30_days_count = Sale.objects.filter(date__gte=last_thirty_sales).count()

    one_year_ago = datetime.now() - timedelta(days=365)

    entries_per_month = Sale.objects.filter(
        date__range=(one_year_ago, datetime.now())
    ).annotate(
        month=TruncMonth('date')
    ).values('month').annotate(count=Count('id')).order_by('month')

    total_entries = sum(entry['count'] for entry in entries_per_month)
    total_months = len(entries_per_month)

    average_entries = total_entries / total_months if total_months > 0 else 0

    # show budget

    current_date = datetime.now()
    current_month = current_date.strftime('%B')
    fiscal_year = current_date.year  # Assuming fiscal year starts in January

    current_month_budget = InfoTable.objects.filter(month=current_month, fiscal_year=fiscal_year).first()
    records_in_fiscal_year = InfoTable.objects.filter(fiscal_year=fiscal_year)
    total_budget = records_in_fiscal_year.aggregate(Sum('budget'))['budget__sum']

    context = {
        'total_sales_value': total_sales_value_formatted,
        'total_annual_sales_formatted': total_annual_sales_formatted,
        'last_30_days_count': last_30_days_count,
        'average_entries': average_entries,
        'current_month_budget':current_month_budget,
        'total_budget':total_budget,
        'prev_12_month':prev_12_month,
        'monthly_sales_list': monthly_sales_list

    }
    return render(request, 'homedash/index.html', context)


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

@login_required(login_url='/authenticate/login/')
def add_sale(request):
    if request.method == 'POST':
        product_ids = request.POST.getlist('product')
        username = request.POST.get('username')
        sale_value = request.POST.get('sale_value')
        remarks = request.POST.get('remarks')

        selected_products = Products.objects.filter(id__in=product_ids)
        user_profile = UserProfile.objects.get(user__username=username)

        new_sale = Sale.objects.create(
            user_profile=user_profile,
            sale_value=sale_value,
            remarks=remarks,
            date=datetime.now()
        )

        new_sale.product.set(selected_products)


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
        if start_date:
            query &= Q(date__gte= start_date)
        if end_date:
            query &= Q(date__lte=end_date)
        if min_price:
            query &= Q(sale_value__gte=min_price)
        if max_price:
            query &= Q(sale_value__lte=max_price)

        results = Sale.objects.filter(query).order_by('-date')

    return render(request, 'homedash/search.html', {'results': results})
