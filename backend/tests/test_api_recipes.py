from collections import OrderedDict
from unittest import TestCase

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from api.serializers import RecipesSerializer, IngredientSerializer, TagSerializer
from recipes.models import Ingredient, Tag, Recipe
from users.models import User


class RecipesApiTestCase(APITestCase):

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
        cls.user_3 = User.objects.create(
            email='test3@example.com',
            username='test_3',
            first_name='test3',
            last_name='test3',
            password='test3',
        )
        cls.ingredient_1 = Ingredient.objects.create(
            name='ingredient_1',
            measurement_unit='pc',
        )
        cls.ingredient_2 = Ingredient.objects.create(
            name='ingredient_2',
            measurement_unit='kg',
        )
        cls.tag_1 = Tag.objects.create(
            name='tag_1',
            color='#f00000',
            slug='tag1'
        )
        cls.tag_2 = Tag.objects.create(
            name='tag_2',
            color='#f00001',
            slug='tag2'
        )
        cls.tag_3 = Tag.objects.create(
            name='tag_3',
            color='#f00002',
            slug='tag3'
        )
        cls.recipe_1 = Recipe.objects.create(
            name='recipe_1',
            text='text_1',
            cooking_time=1,
            author=cls.user_2
        )
        cls.recipe_1.ingredients.add(*[cls.ingredient_1, cls.ingredient_2], through_defaults={'amount': 20.00})
        cls.recipe_1.tags.add(1, 2)
        cls.recipe_2 = Recipe.objects.create(
            name='recipe_2',
            text='text_2',
            cooking_time=2,
            author=cls.user_2
        )
        cls.recipe_2.ingredients.add(cls.ingredient_1, through_defaults={'amount': 30.00})
        cls.recipe_2.tags.add(3)
        cls.recipe_3 = Recipe.objects.create(
            name='recipe_3',
            text='text_3',
            cooking_time=3,
            author=cls.user_3
        )
        cls.recipe_3.ingredients.add(cls.ingredient_2, through_defaults={'amount': 30.00})
        cls.recipe_3.tags.add(2)
        cls.auth_client = APIClient()
        cls.auth_client.force_authenticate(user=cls.user_1)

    def test_recipe_get_list(self):
        url = reverse('api:recipes-list')
        response = self.client.get(url)
        serializer_data = RecipesSerializer([self.recipe_3, self.recipe_2, self.recipe_1], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_recipe_get_detail(self):
        pk = self.recipe_2.id
        url = reverse('api:recipes-detail', kwargs={'id': pk})
        response_auth = self.auth_client.get(url)
        response = self.client.get(url)
        serializer_data = RecipesSerializer(self.recipe_2).data
        self.assertEqual(status.HTTP_200_OK, response_auth.status_code)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response_auth.data)

    def test_recipe_create_recipe(self):
        url = reverse('api:recipes-list')
        data = {
            "ingredients": [
                {
                    "id": 2,
                    "amount": 10
                }
            ],
            "tags": [
                1,
                2
            ],
            "image": ("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAA"
                      "AACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg=="),
            "name": "Recipe_4",
            "text": "string",
            "cooking_time": 1
        }
        response = self.client.post(url, data, format='json')
        response_auth = self.auth_client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response_auth.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Recipe.objects.count(), 4)
        self.assertEqual(Recipe.objects.get(id=4).name, "Recipe_4")

    def test_recipe_update_recipe(self):
        pk = self.recipe_1.id
        url = reverse('api:recipes-detail', kwargs={'id': pk})
        data = {
            "ingredients": [
                {
                    "id": 2,
                    "amount": 10
                }
            ],
            "tags": [
                1,
                2
            ],
            "image": ("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAA"
                      "AACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg=="),
            "name": "Recipe_4",
            "text": "string",
            "cooking_time": 1
        }
        self.auth_client_author = APIClient()
        self.auth_client_author.force_authenticate(user=self.user_2)
        response = self.client.patch(url, data, format='json')
        response_author = self.auth_client_author.patch(url, data, format='json')
        response_auth = self.auth_client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response_author.status_code, status.HTTP_200_OK)
        self.assertEqual(response_auth.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Recipe.objects.get(id=1).name, "Recipe_4")

    def test_recipe_delete_recipe(self):
        pk = self.recipe_1.id
        url = reverse('api:recipes-detail', kwargs={'id': pk})
        self.assertEqual(3, Recipe.objects.count())
        self.auth_client_author = APIClient()
        self.auth_client_author.force_authenticate(user=self.user_2)
        response = self.client.delete(url)
        response_auth = self.auth_client.delete(url)
        response_author = self.auth_client_author.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response_author.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response_auth.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(2, Recipe.objects.count())

    def test_recipe_shopping_list_post(self):
        pk = self.recipe_2.id
        url = reverse('api:recipes-detail', kwargs={'id': pk})
        url_shopping = reverse('api:recipes-shopping-cart', kwargs={'id': pk})
        response_auth_before = self.auth_client.get(url)
        response_auth = self.auth_client.post(url_shopping)
        response_auth_after = self.auth_client.get(url)
        self.assertEqual(status.HTTP_201_CREATED, response_auth.status_code)
        self.assertNotEqual(True, response_auth_before.data['is_in_shopping_cart'])
        self.assertEqual(True, response_auth_after.data['is_in_shopping_cart'])

    def test_recipe_shopping_list_delete(self):
        user = self.user_1
        recipe = self.recipe_2
        user.is_in_shopping_cart.add(recipe)
        pk = self.recipe_2.id
        url = reverse('api:recipes-detail', kwargs={'id': pk})
        url_shopping = reverse('api:recipes-shopping-cart', kwargs={'id': pk})
        response_auth_before = self.auth_client.get(url)
        response_auth = self.auth_client.delete(url_shopping)
        response_auth_after = self.auth_client.get(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response_auth.status_code)
        self.assertEqual(True, response_auth_before.data['is_in_shopping_cart'])
        self.assertNotEqual(True, response_auth_after.data['is_in_shopping_cart'])

    def test_recipe_favorited_post(self):
        pk = self.recipe_2.id
        url = reverse('api:recipes-detail', kwargs={'id': pk})
        url_favorited = reverse('api:recipes-favorite', kwargs={'id': pk})
        response_auth_before = self.auth_client.get(url)
        response_auth = self.auth_client.post(url_favorited)
        response_auth_after = self.auth_client.get(url)
        self.assertEqual(status.HTTP_201_CREATED, response_auth.status_code)
        self.assertNotEqual(True, response_auth_before.data['is_favorited'])
        self.assertEqual(True, response_auth_after.data['is_favorited'])

    def test_recipe_favorited_delete(self):
        user = self.user_1
        recipe = self.recipe_2
        user.is_favorited.add(recipe)
        pk = self.recipe_2.id
        url = reverse('api:recipes-detail', kwargs={'id': pk})
        url_shopping = reverse('api:recipes-favorite', kwargs={'id': pk})
        response_auth_before = self.auth_client.get(url)
        response_auth = self.auth_client.delete(url_shopping)
        response_auth_after = self.auth_client.get(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response_auth.status_code)
        self.assertEqual(True, response_auth_before.data['is_favorited'])
        self.assertNotEqual(True, response_auth_after.data['is_favorited'])

    def test_recipe_search_author(self):
        url = reverse('api:recipes-list')
        response = self.client.get(url, data={'author': 3})
        serializer_data = RecipesSerializer([self.recipe_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_recipe_search_tags(self):
        url = reverse('api:recipes-list')
        response = self.client.get(url, data={'tags': 'tag3'})
        serializer_data = RecipesSerializer([self.recipe_2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_ingredient_get_list(self):
        url = reverse('api:ingredients-list')
        response = self.client.get(url)
        serializer_data = IngredientSerializer([self.ingredient_1, self.ingredient_2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_ingredient_get_detail(self):
        pk = self.ingredient_2.id
        url = reverse('api:ingredients-detail', kwargs={'id': pk})
        response = self.client.get(url)
        serializer_data = IngredientSerializer(self.ingredient_2).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_ingredient_search_name(self):
        url = reverse('api:ingredients-list')
        response = self.client.get(url, data={'name': 'ingredient_2'})
        serializer_data = IngredientSerializer([self.ingredient_2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_tag_get_list(self):
        url = reverse('api:tags-list')
        response = self.client.get(url)
        serializer_data = TagSerializer([self.tag_3, self.tag_2, self.tag_1], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_tag_get_detail(self):
        pk = self.tag_2.id
        url = reverse('api:tags-detail', kwargs={'id': pk})
        response = self.client.get(url)
        serializer_data = TagSerializer(self.tag_2).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)


class RecipeSerializerTestCase(TestCase):
    def test_recipe_serializer(self):
        user_1 = User.objects.create(
            email='test@example.com',
            username='test_1',
            first_name='test',
            last_name='test',
            password='test',
        )
        recipe_1 = Recipe.objects.create(
            name='recipe_1',
            text='text_1',
            image=("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAAC"
                   "XBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg=="),
            cooking_time=1,
            author=user_1
        )
        data = RecipesSerializer(recipe_1).data
        expected_data = {
            'id': 1,
            'tags': [],
            'author': OrderedDict([('email', 'test@example.com'),
                                   ('id', 1),
                                   ('username', 'test_1'),
                                   ('first_name', 'test'),
                                   ('last_name', 'test'),
                                   ('is_subscribed', False)]),
            'ingredients': [],
            'is_favorited': False,
            'is_in_shopping_cart': False,
            'name': 'recipe_1',
            'image': ('/media/data%3Aimage/png%3Bbase64%2CiVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD/9'
                      'fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg%3D%3D'),
            'text': 'text_1',
            'cooking_time': 1,
        }
        self.assertEqual(expected_data, data)

    def test_ingredient_serializer(self):
        ingredient = Ingredient.objects.create(
            name='ingredient_1',
            measurement_unit='pc',
        )
        data = IngredientSerializer(ingredient).data
        expected_data = {
            "id": ingredient.id,
            "name": "ingredient_1",
            "measurement_unit": "pc"
        }
        self.assertEqual(expected_data, data)

    def test_tag_serializer(self):
        tag = Tag.objects.create(
            name='tag_1',
            color='#f00000',
            slug='tag1'
        )
        data = TagSerializer(tag).data
        expected_data = {
            "id": tag.id,
            "name": "tag_1",
            "color": "#f00000",
            "slug": "tag1",
        }
        self.assertEqual(expected_data, data)