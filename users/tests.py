from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import CustomUser
from branches.models import Branch


class UserTests(APITestCase):

    def setUp(self):
        # Create a branch for testing
        self.branch = Branch.objects.create(name="Test Branch", latitude=0.0, longitude=0.0, contact_number="123456789")

        # Create an admin user
        self.admin_user = CustomUser.objects.create_superuser(
            username="admin", email="admin@test.com", password="admin123", user_type="admin"
        )

        # Create a manager user
        self.manager_user = CustomUser.objects.create_user(
            username="manager", email="manager@test.com", password="manager123", user_type="manager", branch=self.branch
        )

        # Create a staff user
        self.staff_user = CustomUser.objects.create_user(
            username="staff", email="staff@test.com", password="staff123", user_type="staff", branch=self.branch
        )

        # Admin login
        response = self.client.post(reverse('token_obtain_pair'), {'username': 'admin', 'password': 'admin123'})
        self.admin_token = response.data['access']

    def test_create_user(self):
        url = reverse('register_user')
        data = {
            "username": "new_user",
            "email": "new_user@test.com",
            "password": "newuser123",
            "user_type": "customer"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_staff_by_admin(self):
        url = reverse('create_staff')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_token)
        data = {
            "username": "new_staff",
            "email": "new_staff@test.com",
            "user_type": "staff",
            "branch": self.branch.pk
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_user_account(self):
        url = reverse('edit_own_account')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_token)
        data = {
            "first_name": "UpdatedAdmin",
            "last_name": "Test"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(CustomUser.objects.get(id=self.admin_user.id).first_name, "UpdatedAdmin")

    def test_delete_user(self):
        url = reverse('delete_user', kwargs={'pk': self.staff_user.pk})
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_token)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CustomUser.objects.filter(id=self.staff_user.id).exists())

    def test_get_user_account(self):
        url = reverse('get_user_account')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.admin_user.email)
