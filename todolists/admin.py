from django.contrib import admin
from .models import TodoList, TodoItem

# Register your models here.
class TodoItemInline(admin.TabularInline):

    model = TodoItem
    extra = 3

class TodoListAdmin(admin.ModelAdmin):

    inlines = [TodoItemInline]

admin.site.register(TodoList, TodoListAdmin)