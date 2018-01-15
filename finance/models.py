from django.contrib.auth.models import Permission, User
from django.db import models

class Income(models.Model):
    INCOME_CHOICES = (
        ('Allowance', 'Allowance'),
        ('Salary', 'Salary'),
        ('Cash', 'Cash'),
        ('Bonus', 'Bonus'),
        ('Other', 'Other'),
    )
    user = models.ForeignKey(User, default=1, on_delete=models.DO_NOTHING,)
    title = models.CharField(max_length=250)
    catogory = models.CharField(max_length=100, choices=INCOME_CHOICES)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title

class Expense(models.Model):
    EXPENSE_CHOICES = (
        ('Food', 'Food'),
        ('Social life', 'Social life'),
        ('Transportation', 'Transportation'),
        ('Household', 'Household'),
        ('Culture', 'Culture'),
        ('Other', 'Other'),
    )
    user = models.ForeignKey(User, default=1, on_delete=models.DO_NOTHING,)
    title = models.CharField(max_length=250)
    catogory = models.CharField(max_length=100, choices=EXPENSE_CHOICES)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title
