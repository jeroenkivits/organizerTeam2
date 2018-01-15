from django.contrib.auth.models import User
from django import forms
from .models import Note

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username','password']


class NoteForm(forms.ModelForm):

    class Meta:
        model = Note
        fields = ['title', 'description',]
