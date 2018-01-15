from django.contrib.auth.models import Permission, User
from django.db import models

class Task(models.Model):
    user = models.ForeignKey(User, default=1, on_delete = models.PROTECT)
    task_name = models.CharField(max_length=250)
    task_done = models.BooleanField(default=False)
    deadline = models.DateField()
    def __str__(self):
        return self.task_name
