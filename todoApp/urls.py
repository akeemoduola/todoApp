"""todoApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/tospics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from todolists.views import Index, TodoLists, SignUpView, TodoListEditView, TodoListAddItemView, TodoListDeleteView, logout_user
from django.contrib.auth import views as auth_views

admin.autodiscover()

urlpatterns = [
    url(r'^$', Index.as_view(), name='index'),
    url(r'^dashboard/$', TodoLists.as_view(), name='todolists'),
    url(r'^signup/$', SignUpView.as_view(), name='signup'),
    url(r'^admin/', admin.site.urls),
    url(r'^todolist/(?P<id>[0-9]+)$',
        TodoListEditView.as_view(), name='edit_todolist'),
    url(r'^todolist-delete/(?P<id>[0-9]+)$',
        TodoListDeleteView.as_view(), name='delete_todolist'),
    url(r'^todolist/(?P<id>[0-9]+)/items$',
        TodoListAddItemView.as_view(), name='add_item'),
    url(r'^logout/$', logout_user, name='logout'),

]
