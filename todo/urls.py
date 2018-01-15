from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

app_name = 'todo'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'index_todo/$', views.index_todo, name='index_todo'),
    url(r'add_task/$', views.add_task, name='add_task'),
    url(r'task/(?P<task_id>[0-9]+)/delete_task/$', views.delete_task, name='delete_task'),
    url(r'task/(?P<task_id>[0-9]+)/delete_task2/$', views.delete_task2, name='delete_task2'),
    url(r'^(?P<task_id>[0-9]+)/task_done/$', views.task_done, name='task_done'),
    url(r'^(?P<task_id>[0-9]+)/task_done2/$', views.task_done2, name='task_done2'),

    url(r'twitter', views.twitter, name='twitter'),
    url(r'facebook', views.facebook, name='facebook'),
    url(r'weather', views.weather, name='weather'),
    url(r'maps', views.maps, name='maps'),
    url(r'startpage', views.startpage, name='startpage'),
    url(r'login', auth_views.login, name='login'),
    url(r'logout', auth_views.logout, name='logout'),
    url(r'signup', views.signup, name='signup'),
    url(r'about', views.about, name='about'),
]
