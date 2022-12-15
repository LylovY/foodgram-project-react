from unittest import TestCase

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from api.serializers import UserSerializer
from users.models import Follow, User


class UsersApiTestCase(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_1 = User.objects.create(
            email='test@example.com',
            username='test_1',
            first_name='test',
            last_name='test',
            password='test',
        )
        cls.user_2 = User.objects.create(
            email='test2@example.com',
            username='test_2',
            first_name='test2',
            last_name='test2',
            password='test2',
        )
        cls.auth_client = APIClient()
        cls.auth_client.force_authenticate(user=cls.user_1)

    def test_get_list(self):
        url = reverse('api:users-list')
        response = self.client.get(url)
        serializer_data = UserSerializer([self.user_2, self.user_1], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_detail(self):
        pk = self.user_2.id
        url = reverse('api:users-detail', kwargs={'id': pk})
        response_auth = self.auth_client.get(url)
        response = self.client.get(url)
        serializer_data = UserSerializer(self.user_2).data
        self.assertEqual(status.HTTP_200_OK, response_auth.status_code)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        self.assertEqual(serializer_data, response_auth.data)

    def test_create_user(self):
        url = reverse('api:users-list')
        data = {
            "email": "vpupkin@yandex.ru",
            "username": "vasya.pupkin",
            "first_name": "Вася",
            "last_name": "Пупкин",
            "password": "adminadmin"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)
        self.assertEqual(User.objects.get(id=3).username, "vasya.pupkin")

    def test_user_me(self):
        url = reverse('api:users-me')
        response_auth = self.auth_client.get(url)
        serializer_data = UserSerializer(self.user_1).data
        self.assertEqual(status.HTTP_200_OK, response_auth.status_code)
        self.assertEqual(serializer_data, response_auth.data)

    def test_user_subscribe(self):
        pk = self.user_2.id
        url = reverse('api:users-detail', kwargs={'id': pk})
        url_subs = reverse('api:users-subscribe', kwargs={'id': pk})
        response_auth_before = self.auth_client.get(url)
        response_auth = self.auth_client.post(url_subs)
        response_auth_after = self.auth_client.get(url)
        self.assertEqual(status.HTTP_201_CREATED, response_auth.status_code)
        self.assertNotEqual(True, response_auth_before.data['is_subscribed'])
        self.assertEqual(True, response_auth_after.data['is_subscribed'])

    def test_user_unsubscribe(self):
        Follow.objects.create(
            user=self.user_1,
            author=self.user_2
        )
        pk = self.user_2.id
        url = reverse('api:users-detail', kwargs={'id': pk})
        url_subs = reverse('api:users-subscribe', kwargs={'id': pk})
        response_auth_before = self.auth_client.get(url)
        response_auth = self.auth_client.delete(url_subs)
        response_auth_after = self.auth_client.get(url)
        self.assertEqual(True, response_auth_before.data['is_subscribed'])
        self.assertNotEqual(True, response_auth_after.data['is_subscribed'])

    def test_user_subscriptions(self):
        queryset_before = Follow.objects.filter(user=self.user_1, author=self.user_2).count()
        Follow.objects.create(
            user=self.user_1,
            author=self.user_2
        )
        queryset_after = Follow.objects.filter(user=self.user_1, author=self.user_2).count()
        self.assertEqual(0, queryset_before)
        self.assertEqual(1, queryset_after)


class UserSerializerTestCase(TestCase):
    def test_serializer(self):
        user_1 = User.objects.create(
            email='test@example.com',
            username='test_1',
            first_name='test',
            last_name='test',
            password='test',
        )
        data = UserSerializer(user_1).data
        expected_data = {
            "email": 'test@example.com',
            "id": user_1.id,
            "username": 'test_1',
            "first_name": 'test',
            "last_name": 'test',
            "is_subscribed": False
        }
        self.assertEqual(expected_data, data)
