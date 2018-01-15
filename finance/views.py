from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.views.generic import View
from .forms import ExpenseForm, IncomeForm
from .models import Income, Expense
from django.contrib.auth import logout
from django.http import JsonResponse
from django.db.models import Q
from datetime import datetime, timedelta
from django.db.models import Sum

# Create your views here.

def index(request, filter_by):
    if not request.user.is_authenticated:
        return render(request, 'todo/startpage.html')
    else:
        income_balance = Income.objects.aggregate(Sum('amount'))
        expense_balance = Expense.objects.aggregate(Sum('amount'))

        food_balance =  Expense.objects.filter(catogory__iexact='food').aggregate(Sum('amount'))['amount__sum']
        social_balance =  Expense.objects.filter(catogory__iexact='social life').aggregate(Sum('amount'))['amount__sum']
        transport_balance =  Expense.objects.filter(catogory__iexact='transportation').aggregate(Sum('amount'))['amount__sum']
        household_balance =  Expense.objects.filter(catogory__iexact='household').aggregate(Sum('amount'))['amount__sum']
        culture_balance =  Expense.objects.filter(catogory__iexact='culture').aggregate(Sum('amount'))['amount__sum']
        other_balance =  Expense.objects.filter(catogory__iexact='other').aggregate(Sum('amount'))['amount__sum']


        incomes = Income.objects.filter(user=request.user).order_by('-id')
        last = incomes[:3]


        expenses = Expense.objects.filter(user=request.user)
        if not expenses and not incomes:
            balance = 0
        elif not incomes:
            balance = - expense_balance['amount__sum']
        elif not expenses:
            balance = income_balance['amount__sum']
        else:
            balance = income_balance['amount__sum'] -  expense_balance['amount__sum']

        if filter_by == 'today':
            incomes = incomes.filter(date__gte=datetime.now())
            expenses = expenses.filter(date__gte=datetime.now())
        if filter_by == 'last_week':
            incomes = incomes.filter(date__gte=datetime.now()-timedelta(days=6))
            expenses = expenses.filter(date__gte=datetime.now()-timedelta(days=6))
        return render(request, 'finance/index.html', {'expenses': expenses, 'incomes' : incomes, 'filter_by': filter_by, 'balance': balance, 'food_balance' : food_balance, 'last' : last})

def dashboard(request):
    if not request.user.is_authenticated:
        return render(request, 'todo/startpage.html')
    else:
        food_balance =  Expense.objects.filter(catogory__iexact='food').aggregate(Sum('amount'))['amount__sum']
        social_balance =  Expense.objects.filter(catogory__iexact='social life').aggregate(Sum('amount'))['amount__sum']
        transport_balance =  Expense.objects.filter(catogory__iexact='transportation').aggregate(Sum('amount'))['amount__sum']
        household_balance =  Expense.objects.filter(catogory__iexact='household').aggregate(Sum('amount'))['amount__sum']
        culture_balance =  Expense.objects.filter(catogory__iexact='culture').aggregate(Sum('amount'))['amount__sum']
        other_balance =  Expense.objects.filter(catogory__iexact='other').aggregate(Sum('amount'))['amount__sum']
        income_total = Income.objects.aggregate(Sum('amount'))['amount__sum']
        expense_total = Expense.objects.aggregate(Sum('amount'))['amount__sum']
        incomes = Income.objects.filter(user=request.user).order_by('-id')
        last_incomes = incomes[:3]
        expenses = Expense.objects.filter(user=request.user).order_by('-id')
        last_expenses = expenses[:3]
        if not expenses and not incomes:
            balance_total = 0
        elif not incomes:
            balance_total = - expense_total
        elif not expenses:
            balance_total = income_total
        else:
            balance_total = income_total -  expense_total
        if balance_total < 0:
            negative = True
            balance_total = abs(balance_total)
        else:
            negative = False

        context = {
        'expenses': expenses,
        'incomes' : incomes,
        'balance_total': balance_total,
        'negative' : negative,
        'last_incomes' : last_incomes,
        'last_expenses' : last_expenses,
        'food_balance' : food_balance,
        'social_balance' : social_balance,
        'transport_balance' : transport_balance,
        'household_balance' : household_balance,
        'culture_balance' : culture_balance,
        'other_balance' : other_balance,
        'income_total' : income_total,
        'expense_total' : expense_total,
        }
        return render(request, 'finance/dashboard.html', context)


def income(request, filter_by):
    if not request.user.is_authenticated:
        return render(request, 'todo/startpage.html')
    else:
        incomes = Income.objects.filter(user=request.user).order_by('-id')
    if filter_by == 'today':
        incomes = incomes.filter(date__gte=datetime.now()-timedelta(days=1))
    if filter_by == 'last_week':
        incomes = incomes.filter(date__gte=datetime.now()-timedelta(days=6))
    return render(request, 'finance/income.html', {'incomes' : incomes, 'filter_by': filter_by,})

def expense(request, filter_by):
    if not request.user.is_authenticated:
        return render(request, 'todo/startpage.html')
    else:
        expenses = Expense.objects.filter(user=request.user).order_by('-id')
    if filter_by == 'today':
        expenses = expenses.filter(date__gte=datetime.now()-timedelta(days=1))
    if filter_by == 'last_week':
        expenses = expenses.filter(date__gte=datetime.now()-timedelta(days=6))
    return render(request, 'finance/expense.html', {'expenses' : expenses, 'filter_by': filter_by,})




def add_income(request):
    if not request.user.is_authenticated:
        return render(request, 'todo/startpage.html')
    else:
        form = IncomeForm(request.POST or None)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()
            incomes =  Income.objects.filter(user=request.user).order_by('-id')
            expenses = Expense.objects.filter(user=request.user)
            income_balance = Income.objects.aggregate(Sum('amount'))
            expense_balance = Expense.objects.aggregate(Sum('amount'))
            if not expenses and not incomes:
                balance = 0
            elif not incomes:
                balance = - expense_balance['amount__sum']
            elif not expenses:
                balance = income_balance['amount__sum']
            else:
                balance = income_balance['amount__sum'] -  expense_balance['amount__sum']
            filter_by = 'all'
            return render(request, 'finance/income.html', {'expenses': expenses, 'incomes' : incomes, 'filter_by': filter_by, 'balance': balance})
        context = {
            "form": form,
        }
        return render(request, 'finance/add_income.html', context)

def add_expense(request):
    if not request.user.is_authenticated:
        return render(request, 'todo/startpage.html')
    else:
        form = ExpenseForm(request.POST or None)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            expenses = Expense.objects.filter(user=request.user).order_by('-id')
            incomes = Income.objects.filter(user=request.user)
            income_balance = Income.objects.aggregate(Sum('amount'))
            expense_balance = Expense.objects.aggregate(Sum('amount'))
            if not expenses and not incomes:
                balance = 0
            elif not incomes:
                balance = - expense_balance['amount__sum']
            elif not expenses:
                balance = income_balance['amount__sum']
            else:
                balance = income_balance['amount__sum'] -  expense_balance['amount__sum']

            filter_by = 'all'
            return render(request, 'finance/expense.html',{'expenses': expenses, 'incomes' : incomes, 'filter_by': filter_by, 'balance': balance})
        context = {
            "form": form,
        }
        return render(request, 'finance/add_expense.html', context)
