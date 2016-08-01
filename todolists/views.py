from django.shortcuts import render
from django.views.generic import View
from .models import TodoList

# Create your views here.

class Index(View):
    def get(self, request):
        params = dict()
        todolists = TodoList.objects.all()
        params["todolists"] = todolists
        return render(request, 'todolists.html', params)