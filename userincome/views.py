from locale import currency
from unicodedata import category
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import UserIncome, Source
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
import json
from django.http import JsonResponse
from userpreferences.models import Userpreference
import datetime

@login_required(login_url='/authentication/login')
def index(request):
    sources = Source.objects.all()
    income = UserIncome.objects.filter(owner=request.user)
    paginator = Paginator(income,5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator,page_number)
    # currency = Userpreference.objects.get(user=request.user).currency
    currency = Userpreference.objects.get(user=request.user).currency
    context = {
        'income' : income,
        'page_obj' : page_obj,
        'currency' : currency,
    }
    return render(request,'income/index.html',context)
 
def add_income(request):
    sources = Source.objects.all()
    
    context = {
            'sources' : sources,
            'values': request.POST
        }
    if request.method == 'GET':
        
        return render(request,'income/add_income.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']
        
        if not amount:
            messages.error(request,'Amount is required')  
            return render(request,'income/add_income.html', context)

    
        description = request.POST['description']
        source = request.POST['source']
        date = request.POST['income_date']

        if not description:
            messages.error(request,'Description is required')  
            return render(request,'income/add_income.html', context)

        if not date:
            messages.error(request,'Date is required')  
            return render(request,'income/add_income.html', context)

        UserIncome.objects.create(owner= request.user, amount = amount, description = description, source = source, date = date)
        messages.success(request,'Income added')
        return redirect('income')

def income_edit(request,id):
    income = UserIncome.objects.get(pk=id)
    sources = Source.objects.all()
    context = {
        'income' : income,
        'values' : income,
        'sources' : sources
    }
    if request.method == 'GET':
        return render(request,'income/edit_income.html',context)
    if request.method == 'POST':
        amount = request.POST['amount']
        
        if not amount:
            messages.error(request,'Amount is required')  
            return render(request,'income/edit_income.html', context)

    
        description = request.POST['description']
        source = request.POST['source']
        date = request.POST['income_date']

        if not description:
            messages.error(request,'Description is required')  
            return render(request,'income/edit_income.html', context)

        if not date:
            messages.error(request,'Date is required')  
            return render(request,'income/edit_income.html', context)

        UserIncome.objects.create(owner= request.user, amount = amount, description = description, source = source, date = date)
        income.owner = request.user
        income.amount = amount
        income.description = description
        income.source = source
        income.date = date
        income.save()
        messages.success(request,'Income Updated')
        return redirect('income')
        messages.info(request,'Handling post form')
        return render(request,'expenses/edit_expense.html',context)


def delete_income(request,id):
    income = UserIncome.objects.get(pk=id)
    income.delete()
    messages.success(request,'Income removed')
    return redirect('income')

def income_source_summary(request):
    todays_date = datetime.date.today()
    six_months_ago = todays_date - datetime.timedelta(days = 30*6)
    income = UserIncome.objects.filter(owner = request.user,date__gte = six_months_ago, date__lte = todays_date)
    finalrep = {}
    
    def get_source(income):
        return income.source
        
    sources_lists = list(set(map(get_source, income)))
    

    def get_income_source_amount(source):
        amount = 0
        filtered_by_source = income.filter(source = source)

        for item in filtered_by_source:
            amount = amount + item.amount

        return amount


    for x in income:
        for y in sources_lists:
            finalrep[y] = get_income_source_amount(y)


    return JsonResponse({'Income_source_data' : finalrep}, safe = False)


def stats_view(request):
    return render(request,'income/statsincome.html')
