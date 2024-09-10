
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from menu.models import Menu
from branches.models import Branch

User = get_user_model()


class MenuTests(TestCase):
    def setUp(self):

        self.branch = Branch.objects.create(
            name='Test Branch',
            address='Test Address',
            longitude=12.345,
            latitude=67.890
        )

        # Create users with unique email addresses
        self.user_admin = User.objects.create_user(username='admin', email='admin@example.com',
                                                   password='adminpassword', user_type='admin')
        self.user_manager = User.objects.create_user(username='manager', email='manager@example.com',
                                                     password='managerpassword', user_type='manager',
                                                     branch=self.branch)
        self.user_staff = User.objects.create_user(username='staff', email='staff@example.com',
                                                   password='staffpassword', user_type='staff', branch=self.branch)
        self.user_customer = User.objects.create_user(username='customer', email='customer@example.com',
                                                      password='customerpassword', user_type='customer')

        self.client = APIClient()

    def authenticate_user(self, user):
        self.client.force_authenticate(user=user)

    def test_create_menu_admin(self):
        self.authenticate_user(self.user_admin)
        response = self.client.post(reverse('create_menu'), {
            'name': 'Test Menu',
            'description': 'Test Description',
            'price': '9.99',
            'branch': self.branch.id,
            'is_available': True,
            'category': 'Test Category',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('menu', response.data)

    def test_create_menu_manager(self):
        self.authenticate_user(self.user_manager)
        response = self.client.post(reverse('create_menu'), {
            'name': 'Test Menu',
            'description': 'Test Description',
            'price': '9.99',
            'branch': self.branch.id,
            'is_available': True,
            'category': 'Test Category',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('menu', response.data)

    def test_create_menu_customer(self):
        self.authenticate_user(self.user_customer)
        response = self.client.post(reverse('create_menu'), {
            'name': 'Test Menu',
            'description': 'Test Description',
            'price': '9.99',
            'branch': self.branch.id,
            'is_available': True,
            'category': 'Test Category',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_menu_items_admin(self):
        self.authenticate_user(self.user_admin)
        response = self.client.get(reverse('get_menu_items'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_menu_items_manager(self):
        self.authenticate_user(self.user_manager)
        response = self.client.get(reverse('get_menu_items'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_menu_item(self):
        self.authenticate_user(self.user_manager)
        menu = Menu.objects.create(
            name='Menu to Delete',
            description='Description',
            price='10.00',
            branch=self.branch,
            is_available=True,
            category='Category'
        )
        response = self.client.delete(reverse('delete_menu_item', args=[menu.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Menu.objects.filter(id=menu.id).exists())
