from django.contrib.auth.models import User
from django import forms
from .models import Task

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username','password']


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['task_name', 'deadline']
