from django.contrib.auth.models import User
from django import forms
from .models import Income, Expense

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username','password']


class IncomeForm(forms.ModelForm):

    class Meta:
        model = Income
        fields = ['title', 'catogory', 'amount',]

class ExpenseForm(forms.ModelForm):

    class Meta:
        model = Expense
        fields = ['title', 'catogory', 'amount']
