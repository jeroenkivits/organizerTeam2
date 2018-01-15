from django.conf.urls import url
from . import views

app_name = 'notes'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^details/(?P<note_id>[0-9]+)/$', views.details, name='details'),
    url(r'^details2/(?P<note_id>[0-9]+)/$', views.details2, name='details2'),
    url(r'add_note/$', views.add_note, name='add_note'),
    url(r'^(?P<note_id>[0-9]+)/delete_note/$', views.delete_note, name='delete_note'),
    url(r'^(?P<note_id>[0-9]+)/delete_note2/$', views.delete_note2, name='delete_note2'),
]
