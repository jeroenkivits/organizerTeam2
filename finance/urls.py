from django.conf.urls import url
from . import views

app_name = 'finance'

urlpatterns = [
    url(r'income/(?P<filter_by>[a-zA_Z]+)/$', views.income, name='income'),
    url(r'expense/(?P<filter_by>[a-zA_Z]+)/$', views.expense, name='expense'),
    url(r'dashboard/$', views.dashboard, name='dashboard'),
    url(r'add_income/$', views.add_income, name='add_income'),
    url(r'add_expense/$', views.add_expense, name='add_expense'),
]
