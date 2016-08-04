"""Test for the todolist views"""
import datetime
from django.test.utils import setup_test_environment
setup_test_environment()
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from todolists.models import TodoList
from todolists.models import TodoItem


class TodoListViewTest(TestCase):
    """This is the set up test for todolist view
    """

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='test',
            password='test'
        )
        self.user.set_password('test')
        self.user.save()
        self.login = self.client.login(
            username='test', password='test')
        self.todolist = TodoList.objects.create(
            name='test_todolist', description='desc', owner=self.user)

        self.todoitem = TodoItem.objects.create(
            todolist=self.todolist, text='a new desc', completed=False, due_at=datetime.datetime.now())

    def tearDown(self):
        User.objects.all().delete()
        TodoList.objects.all().delete()
        TodoItem.objects.all().delete()

    def test_can_reach_todolists_page(self):
        """ Test if logged in user can reach the todolist collection page
        """
        response = self.client.get(
            reverse('todolists'))
        self.assertEqual(response.status_code, 200)

    def test_can_create_todotlist(self):
        """ Test user can create a todolist
        """
        data = {'name': 'sales', 'description': 'olx'}
        url = reverse('todolists')
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)
