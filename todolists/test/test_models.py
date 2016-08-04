""" Test cases for todolist models """

from django.test import TestCase
from todolists.models import TodoList
from django.contrib.auth.models import User


class TodoListTestModels(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            username='inioluwafageyinbo', password='codango')
        self.todolist = TodoList.objects.create(
            name='test todo',
            owner=self.user,
            description='help file'
        )

    def tearDown(self):
        User.objects.all().delete()
        TodoList.objects.all().delete()

    def test_can_get_todolist(self):
        todolist = str(self.id)
        self.assertIsNotNone(todolist)
