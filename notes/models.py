from django.contrib.auth.models import Permission, User
from django.db import models

class Note(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.DO_NOTHING,)
    title = models.CharField(max_length=250)
    date = models.DateField(auto_now_add=True)
    description = models.CharField(max_length=1000)
    def __str__(self):
        return self.title
