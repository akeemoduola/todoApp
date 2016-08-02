import datetime
from django.db import models
from django.utils import timezone
from django.contrib import auth



class TodoList(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100)
    owner = models.ForeignKey(auth.models.User, related_name='todolists')

    def __str__(self):
        return self.name

class TodoItem(models.Model):
    todolist = models.ForeignKey(TodoList, on_delete=models.CASCADE, related_name="items")
    text = models.CharField(max_length=200)
    created_at = models.DateTimeField('date created',auto_now_add=True)
    due_at = models.DateTimeField('due date')
    completed = models.BooleanField(default=False)