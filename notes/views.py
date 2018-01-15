from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.views.generic import View
from finance.models import Income, Expense
from todo.models import Task
from .models import Note
from .forms import UserForm, NoteForm
from django.contrib.auth import logout
from django.http import JsonResponse
from django.db.models import Q
from datetime import datetime, timedelta
from django.db.models import Sum


def index(request):
    if not request.user.is_authenticated:
        return render(request, 'todo/startpage.html')
    else:
        notes = Note.objects.filter(user=request.user)
        return render(request, 'notes/index.html', {'notes': notes})

def details(request, note_id):
    if not request.user.is_authenticated:
        return render(request, 'todo/startpage.html')
    else:
        note = get_object_or_404(Note, pk=note_id)
        return render(request, 'notes/details.html', {'note': note,})

def details2(request, note_id):
    if not request.user.is_authenticated:
        return render(request, 'todo/startpage.html')
    else:
        note = get_object_or_404(Note, pk=note_id)
        return render(request, 'notes/details2.html', {'note': note,})

def add_note(request):
    if not request.user.is_authenticated:
        return render(request, 'todo/startpage.html')
    else:
        form = NoteForm(request.POST or None)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            notes = Note.objects.filter(user=request.user)
            return render(request, 'notes/index.html', {'notes': notes})
        context = {
            "form": form,
        }
        return render(request, 'notes/add_note.html', context)

def delete_note(request, note_id):
    note = Note.objects.get(pk=note_id)
    note.delete()
    notes = Note.objects.filter(user=request.user)
    return render(request, 'notes/index.html', {'notes': notes})

def delete_note2(request, note_id):
    if not request.user.is_authenticated:
        return render(request, 'todo/startpage.html')
    else:
        note = Note.objects.get(pk=note_id)
        note.delete()
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
