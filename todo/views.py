from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate

from django.views.generic import View
from .forms import UserForm, TaskForm
from finance.models import Income, Expense
from notes.models import Note
from .models import Task
from django.contrib.auth import logout
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from datetime import datetime, timedelta
from django.db.models import Sum

def task_done(request, task_id):
    task = Task.objects.get(pk=task_id)
    if task.task_done:
        task.task_done = False
    else:
        task.task_done = True
    task.save()
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'todo/index_todo.html', {'tasks': tasks})

def task_done2(request, task_id):
    if not request.user.is_authenticated:
        return render(request, 'todo/startpage.html')
    else:
        task = Task.objects.get(pk=task_id)
        if task.task_done:
            task.task_done = False
        else:
            task.task_done = True
        notes = Note.objects.filter(user=request.user)
        task.save()
        tasks = Task.objects.filter(user=request.user)
        food_balance =  Expense.objects.filter(catogory__iexact='food').aggregate(Sum('amount'))['amount__sum']
        social_balance =  Expense.objects.filter(catogory__iexact='social life').aggregate(Sum('amount'))['amount__sum']
        transport_balance =  Expense.objects.filter(catogory__iexact='transportation').aggregate(Sum('amount'))['amount__sum']
        household_balance =  Expense.objects.filter(catogory__iexact='household').aggregate(Sum('amount'))['amount__sum']
        culture_balance =  Expense.objects.filter(catogory__iexact='culture').aggregate(Sum('amount'))['amount__sum']
        other_balance =  Expense.objects.filter(catogory__iexact='other').aggregate(Sum('amount'))['amount__sum']
        income_total = Income.objects.aggregate(Sum('amount'))['amount__sum']
        expense_total = Expense.objects.aggregate(Sum('amount'))['amount__sum']
        if expense_total is None:
            expense_total = 0.00
        if income_total is None:
            income_total = 0.00
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
        'tasks' : tasks,
        'notes' : notes,
        }
        return render(request, 'todo/index.html', context)

def add_task(request):
    if not request.user.is_authenticated:
        return render(request, 'todo/startpage.html')
    else:
        form = TaskForm(request.POST or None)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            tasks = tasks = Task.objects.filter(user=request.user)
            return render(request, 'todo/index_todo.html', {'tasks': tasks})
        context = {
            "form": form,
        }
        return render(request, 'todo/add_task.html', context)


def index_todo(request):
    if not request.user.is_authenticated:
        return render(request, 'todo/startpage.html')
    else:
        tasks = Task.objects.filter(user=request.user)
        return render(request, 'todo/index_todo.html', {'tasks': tasks})


def delete_task(request, task_id):
    task = Task.objects.get(pk=task_id)
    task.delete()
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'todo/index_todo.html', {'tasks': tasks})

def delete_task2(request, task_id):
    if not request.user.is_authenticated:
        return render(request, 'todo/startpage.html')
    else:
        notes = Note.objects.filter(user=request.user)
        task = Task.objects.get(pk=task_id)
        task.delete()
        tasks = Task.objects.filter(user=request.user)
        food_balance =  Expense.objects.filter(catogory__iexact='food').aggregate(Sum('amount'))['amount__sum']
        social_balance =  Expense.objects.filter(catogory__iexact='social life').aggregate(Sum('amount'))['amount__sum']
        transport_balance =  Expense.objects.filter(catogory__iexact='transportation').aggregate(Sum('amount'))['amount__sum']
        household_balance =  Expense.objects.filter(catogory__iexact='household').aggregate(Sum('amount'))['amount__sum']
        culture_balance =  Expense.objects.filter(catogory__iexact='culture').aggregate(Sum('amount'))['amount__sum']
        other_balance =  Expense.objects.filter(catogory__iexact='other').aggregate(Sum('amount'))['amount__sum']
        income_total = Income.objects.aggregate(Sum('amount'))['amount__sum']
        expense_total = Expense.objects.aggregate(Sum('amount'))['amount__sum']
        if expense_total is None:
            expense_total = 0.00
        if income_total is None:
            income_total = 0.00
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
        'tasks' : tasks,
        'notes' : notes,
        }
        return render(request, 'todo/index.html', context)

def add_task(request):
    if not request.user.is_authenticated:
        return render(request, 'todo/startpage.html')
    else:
        form = TaskForm(request.POST or None)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            tasks = tasks = Task.objects.filter(user=request.user)
            return render(request, 'todo/index_todo.html', {'tasks': tasks})
        context = {
            "form": form,
        }
        return render(request, 'todo/add_task.html', context)

def twitter(request):
    if not request.user.is_authenticated:
        return render(request, 'todo/startpage.html')
    else:
        return render(request, 'todo/twitter.html')

def facebook(request):
    if not request.user.is_authenticated:
        return render(request, 'todo/startpage.html')
    else:
        return render(request, 'todo/facebook.html')

def weather(request):
    if not request.user.is_authenticated:
        return render(request, 'todo/startpage.html')
    else:
        return render(request, 'todo/weather.html')

def maps(request):
    if not request.user.is_authenticated:
        return render(request, 'todo/startpage.html')
    else:
        return render(request, 'todo/maps.html')

def startpage(request):
    return render(request, 'todo/startpage.html')

def login(request):
    return render(request, 'todo/index.html')

def logout(request):
    logout(request)
    return render(request, 'registration/logged_out.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request)
            return render(request, 'todo/index.html')
    else:
        form = UserCreationForm()
    return render(request, 'todo/signup.html', {'form': form})

def about(request):
    if not request.user.is_authenticated:
        return render(request, 'todo/login.html')
    else:
        return render(request, 'todo/about.html')

def index(request):
    if not request.user.is_authenticated:
        return render(request, 'todo/startpage.html')
    else:
        notes = Note.objects.filter(user=request.user)
        tasks = Task.objects.filter(user=request.user)
        food_balance =  Expense.objects.filter(catogory__iexact='food').aggregate(Sum('amount'))['amount__sum']
        social_balance =  Expense.objects.filter(catogory__iexact='social life').aggregate(Sum('amount'))['amount__sum']
        transport_balance =  Expense.objects.filter(catogory__iexact='transportation').aggregate(Sum('amount'))['amount__sum']
        household_balance =  Expense.objects.filter(catogory__iexact='household').aggregate(Sum('amount'))['amount__sum']
        culture_balance =  Expense.objects.filter(catogory__iexact='culture').aggregate(Sum('amount'))['amount__sum']
        other_balance =  Expense.objects.filter(catogory__iexact='other').aggregate(Sum('amount'))['amount__sum']
        income_total = Income.objects.aggregate(Sum('amount'))['amount__sum']
        expense_total = Expense.objects.aggregate(Sum('amount'))['amount__sum']
        if expense_total is None:
            expense_total = 0.00
        if income_total is None:
            income_total = 0.00
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
        'tasks' : tasks,
        'notes' : notes,
        }
        return render(request, 'todo/index.html', context)
