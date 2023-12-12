from datetime import timezone, timedelta
from urllib import request

from django.contrib.auth.models import User
import calendar
from django.db.models.functions import ExtractMonth

from django.db.models import Q

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
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
from django.http import JsonResponse


# Sales person chart
def category_chart():
    sales_by_category= SalesCategory.objects.annotate(
        total_sale_value=Sum('sales_category_products__sale_product__sale_value')
    ).values('type', 'total_sale_value')

    return sales_by_category

def salesperson_chart(request):
    user = request.user
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    if request.user.user_profile.role_type == "Salesperson":
        user_sales = Sale.objects.filter(user_profile=user.user_profile,date__range=(start_date, end_date)).values(
            'user_profile__full_name').annotate(
            total_sales=Sum('sale_value')).order_by('user_profile__full_name')

    else:
        user_sales = Sale.objects.filter(date__range=(start_date, end_date)).values(
            'user_profile__full_name').annotate(
            total_sales=Sum('sale_value')).order_by('user_profile__full_name')

    user_sales_list = list(user_sales)
    salesperson_name_list = []
    salesperson_value_list = []
    for salesperson in user_sales_list:
        salesperson_name_list.append(salesperson['user_profile__full_name'])
        salesperson_value_list.append(int(salesperson['total_sales']))

    return salesperson_name_list, salesperson_value_list

#Chart for salesperson
def Salesperson_sale(request):
    user = request.user
    current_month = datetime.now().month
    current_year = datetime.now().year

    monthly_sales = (Sale.objects.filter(
        user_profile=user.user_profile,
        date__year=current_year).annotate(month=ExtractMonth('date')).values('month').annotate(
        total_sale=Sum('sale_value')))

    month_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    monthly_sale_data = [0] * 12
    for entry in monthly_sales:
        month_index = entry['month'] - 1
        monthly_sale_data[month_index] = int(entry['total_sale'])

    return month_list, monthly_sale_data

# CHART
def get_chart_data():
    monthly_sales = Sale.objects.annotate(
        month=TruncMonth('date')
    ).values('month').annotate(
        total_sales=Sum('sale_value')
    ).order_by('month')
    month_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    monthly_sales_list = [0] * 12
    for data in monthly_sales:
        monthly_sales_list[data['month'].month - 1] = (int(data['total_sales']))

    return month_list, monthly_sales_list

# MONTHLY REVENUE
def monthly_revenue():
    last_thirty_days = datetime.now() - timedelta(days=30)
    total_sales = Sale.objects.filter(date__gte=last_thirty_days).aggregate(sum_sale=Sum('sale_value'))

    total_sales_value = total_sales['sum_sale'] or 0
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    total_sales_value_formatted = locale.format_string("%d", total_sales_value, grouping=True)

    return total_sales_value_formatted

# YEARLY REVENUE
def yearly_revenue():
    current_year = datetime.now().year
    start_date = datetime(current_year, 1, 1)
    end_date = datetime(current_year, 12, 31)
    total_annual_sales = Sale.objects.filter(date__range=(start_date, end_date)).aggregate(sum_sale=Sum('sale_value'))

    total_annual_sales_value = total_annual_sales['sum_sale'] or 0

    total_annual_sales_formatted = locale.format_string("%d", total_annual_sales_value, grouping=True)

    return total_annual_sales_formatted


# NUMBER OF SALES
def number_of_sales():
    last_thirty_sales = datetime.now() - timedelta(days=30)
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
    return last_30_days_count, average_entries

# SHOW BUDGET
def show_budget():
    current_date = datetime.now()
    current_month = current_date.strftime('%B')
    fiscal_year = current_date.year

    current_month_budget = InfoTable.objects.filter(month=current_month, fiscal_year=fiscal_year).first()
    records_in_fiscal_year = InfoTable.objects.filter(fiscal_year=fiscal_year)
    total_budget = records_in_fiscal_year.aggregate(Sum('budget'))['budget__sum']

    return current_month_budget, total_budget


@login_required(login_url='/authenticate/login/')
def home(request):
    prev_12_month, monthly_sales_list = get_chart_data()
    if not request.user.is_superuser:
        if request.user.user_profile.role_type == "Salesperson":
            prev_12_month, monthly_sales_list = Salesperson_sale(request)
    total_sales_value_formatted = monthly_revenue()
    total_annual_sales_formatted = yearly_revenue()
    last_30_days_count, average_entries = number_of_sales()
    current_month_budget, total_budget = show_budget()
    sales_person_name_list, sales_person_value_list = salesperson_chart(request)
    sales_by_category = category_chart()
    print(sales_by_category)


    month_list, monthly_sales_list_s = Salesperson_sale(request)

    context = {
        'total_sales_value': total_sales_value_formatted,
        'total_annual_sales_formatted': total_annual_sales_formatted,
        'last_30_days_count': last_30_days_count,
        'average_entries': average_entries,
        'current_month_budget': current_month_budget,
        'total_budget': total_budget,
        'prev_12_month': prev_12_month,
        'monthly_sales_list': monthly_sales_list,
        'sales_person_name_list': sales_person_name_list,
        'sales_person_value_list': sales_person_value_list

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
                   'add_category': add_category, })


@login_required(login_url='/authenticate/login/')
def delete_sales_category(request, category_id):
    SalesCategory.objects.get(pk=category_id)

    SalesCategory.objects.get(pk=category_id).delete()
    return redirect('sales_category')


@login_required(login_url='/authenticate/login/')
def view_category(request, category_id):
    sales_category = SalesCategory.objects.get(pk=category_id)
    products = Products.objects.filter(sales_category=sales_category)

    if request.method == 'POST':
        dict = {
            'p_name': request.POST.get('p_name'),
            'price': request.POST.get('price'),
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

        selected_products = Products.objects.get(id__in=product_ids)
        user_profile = UserProfile.objects.get(user__username=username)

        new_sale = Sale.objects.create(
            user_profile=user_profile,
            sale_value=sale_value,
            remarks=remarks,
            date=datetime.now()
        )

        new_sale.product = selected_products
        new_sale.save()


        return redirect('add_sale')

    else:
        products = Products.objects.all()
        user_profiles = UserProfile.objects.all()

    return render(request, 'homedash/add_sale.html', {'products': products, 'user_profiles': user_profiles})


@login_required(login_url='/authenticate/login/')
def search(request):
    if request.method == 'GET':
        username = request.GET.get('username', '')
        product_id = request.GET.get('product_id', '')
        start_date = request.GET.get('start_date', '')
        end_date = request.GET.get('end_date', '')
        min_price = request.GET.get('min_price', '')
        max_price = request.GET.get('max_price', '')

        query = Q()

        if username:
            query &= Q(user_profile__user__username=username)
        if product_id:
            query &= Q(product__id=product_id)
        if start_date:
            query &= Q(date__gte=start_date)
        if end_date:
            query &= Q(date__lte=end_date)
        if min_price:
            query &= Q(sale_value__gte=min_price)
        if max_price:
            query &= Q(sale_value__lte=max_price)

        results = Sale.objects.filter(query).order_by('-date')

    return render(request, 'homedash/search.html', {'results': results})



@login_required(login_url='/authenticate/login/')
def update_sale(request, sale_id):
    sale = Sale.objects.get(pk=sale_id)

    if request.method == 'POST':
        username = request.POST.get('username')
        user_profile = UserProfile.objects.get(user__username=username)
        sale.user_profile = user_profile

        sale.sale_value = request.POST.get('sale_value')
        sale.remarks = request.POST.get('remarks')

        selected_product_id = request.POST.get('product')
        product_instance = get_object_or_404(Products, id=selected_product_id)
        sale.product = product_instance

        sale.save()
        return redirect('search')

    user_profiles = UserProfile.objects.all()
    all_products = Products.objects.all()

    return render(request, 'homedash/update_sale.html', {'sale': sale, 'user_profiles': user_profiles, 'all_products': all_products})


@login_required(login_url='/authenticate/login/')
def add_budget(request):
    if request.method == 'POST':
        fiscal_year = request.POST.get('fiscal_year')
        month = request.POST.get('month')
        budget = request.POST.get('budget')

        info_entry = InfoTable.objects.create(
            fiscal_year=fiscal_year,
            month=month,
            budget=budget
        )

        info_entry.save()
        return redirect('add_budget')

        # Pass month choices to the template
    month_choices = InfoTable._meta.get_field('month').choices

    info_table = InfoTable.objects.all()

    return render(request, 'homedash/add_budget.html', {'info_table':info_table, 'month_choices': month_choices})