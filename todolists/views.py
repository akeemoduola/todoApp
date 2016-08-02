from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from todolists.forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login
from django.template import RequestContext
from todolists.models import TodoList, TodoItem
from todolists.forms import TodoListForm, TodoItemForm


# Create your views here.
def url_redirect(request):
    """Utility function for url redirect
    """
    url = request.META.get('HTTP_REFERER') if request.META.get(
        'HTTP_REFERER') is not None else '/dashboard'
    return redirect(
        url,
        context_instance=RequestContext(request)
    )

class Index(View):

    def get(self, request):
        login_form = LoginForm()
        return render(request, 'index.html', {'login_form': login_form})

    def post(self, request, *args, **kwargs):

        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            print(user)
            if not request.POST.get('remember_me'):
                request.session.set_expiry(0)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, 'Successfully Logged In')
                    return redirect(
                        '/dashboard',
                        context_instance=RequestContext(request)
                    )
            else:
                # redirects with a flash message if user details is invalid
                messages.error(request, 'Username and password incorrect')
                return url_redirect(request)
        else:
            context = super(Index, self).get_context_data(**kwargs)
            context['loginform'] = form
            return render(request, self.template_name, context)


class TodoLists(LoginRequiredMixin, View):
    def get(self, request):
        params = {
            "todolists": request.user.todolists.all()
        }
        return render(request, 'todolists.html', params)

    """
    Creates a new TodoList
    """
    def post(self, request, **kwargs):
        form = TodoListForm(request.POST)
        todolist = form.save(commit=False)
        todolist.owner = request.user
        todolist.save()
        messages.success(request, todolist.name + ' Successfully created')
        return url_redirect(request)

class TodoListEditView(LoginRequiredMixin, View):

    """Edits a particular TodoList
    """
    template_name = 'todolist.html'

    def get(self, request, **kwargs):
        # Gets all the item for a particular TodoList
        todolist_id = kwargs['id']
        todolist = TodoList.objects.filter(id=todolist_id).first()
        items = todolist.items
        context = {}
        context['todoitems'] = items
        context['todolist'] = TodoList
        context['new_item'] = TodoItemForm(auto_id=False)
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        # edits the TodoList name , description or theme
        todolist_id = kwargs['id']
        todolist = TodoList.objects.filter(id=todolist_id).first()
        TodoList.name = request.POST['name']
        TodoList.description = request.POST['description']
        if 'color' in request.POST:
            TodoList.color = request.POST['color']

        TodoList.save()
        messages.success(request, TodoList.name + ' updated')
        return url_redirect(request)


class TodoListAddItemView(LoginRequiredMixin, View):

    """Adds an item to a TodoList collection
    """

    def post(self, request, **kwargs):
        todolist_id = kwargs['id']
        todolist_id = TodoList.objects.filter(id=todolist_id).first()
        form = TodoItemForm(request.POST)
        item = form.save(commit=False)
        item.TodoList = TodoList
        item.done = False
        item.save()
        messages.success(request, item.name + ' Added to ' + TodoList.name)
        return url_redirect(request)


class TodoListDeleteView(LoginRequiredMixin, View):

    """ Deletes a TodoList item 
    """

    def post(self, request, **kwargs):
        todolist_id = kwargs['id']
        todolist = TodoList.objects.filter(id=todolist_id).first()
        TodoList.delete()
        messages.success(request, 'Successfully Deleted')
        return url_redirect(request)

class SignUpView(View):

    """signup page view
    """
    template_name = 'registration/register.html'

    def get(self, request, **kwargs):
        context = {}
        context['registerform'] = RegisterForm(auto_id=False)
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(username=request.POST['username'],
                                    password=request.POST['password'])
            login(request, new_user)
            messages.success(
                request, 'Welcome, you can start creating your todolists collection by clicking on the icon above')
            return redirect(
                '/dashboard',
                context_instance=RequestContext(request)
            )
        else:

            context ={}
            context['form_errors'] = form.errors
            context['registerform'] = form
            return render(request, self.template_name, context)


class ItemDeleteView(LoginRequiredMixin, View):

    """This deletes the item
    """

    def post(self, request, **kwargs):
        item_id = kwargs['id']
        item = TodoItem.objects.filter(id=item_id).first()
        item.delete()
        messages.success(request, 'Successfully deleted')
        return url_redirect(request)


class ItemDoneView(LoginRequiredMixin, View):

    """marks a bucketlist item as done or not done
    """

    def post(self, request, **kwargs):
        item_id = kwargs['id']
        item = TodoItem.objects.filter(id=item_id).first()
        if item.completed is True:
            item.done = False
            messages.error(request, item.name + ' Marked as not done')

        else:
            item.completed = True
            messages.success(request, item.name + ' Marked as done')

        item.save()
        return url_redirect(request)


class ItemEditView(LoginRequiredMixin, View):

    """Edits the description and name of an item
    """

    def post(self, request, **kwargs):
        item_id = kwargs['id']
        item = TodoItem.objects.filter(id=item_id).first()
        item.text = request.POST['text']
        item.completed = request.POST['completed']
        item.due_at = request.POST['due_at']
        item.save()
        messages.success(request, item.name + ' Successfully updated')
        return url_redirect(request)