from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from users.models import CustomUser
from branches.models import Branch, BranchImage


class BranchTests(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.admin_user = CustomUser.objects.create_user(username='admin', password='admin123', user_type='admin')
        self.client.force_authenticate(user=self.admin_user)

        self.branch = Branch.objects.create(
            name='Test Branch',
            address='123 Test St',
            contact_number='1234567890',
            longitude=0.0,
            latitude=0.0,
            description='A test branch.'
        )

    def test_create_branch(self):
        url = reverse('create_branch')
        data = {
            'name': 'New Branch',
            'address': '456 New St',
            'contact_number': '0987654321',
            'longitude': 1.0,
            'latitude': 1.0,
            'description': 'A new branch.'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_images_to_branch(self):
        url = reverse('add_images_to_branch', kwargs={'branch_id': self.branch.pk})

        image_file = SimpleUploadedFile(
            name='test_image.jpg',
            content=open('/Users/erandalakshan/Downloads/istockphoto-1295387240-612x612.jpg', 'rb').read(),
            content_type='image/jpeg'
        )

        data = {
            'images': [image_file]
        }

        # Make the request
        response = self.client.post(url, data, format='multipart')

        # Check response
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_branch(self):
        url = reverse('update_branch', kwargs={'pk': self.branch.pk})
        data = {'name': 'Updated Branch'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_branch(self):
        url = reverse('delete_branch', kwargs={'pk': self.branch.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_branch_image(self):
        image = BranchImage.objects.create(branch=self.branch, image_url='https://example.com/image.jpg')
        url = reverse('delete_branch_image', kwargs={'image_id': image.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
