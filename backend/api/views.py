from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import Ingredient, Recipe, Tag
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from users.models import Follow, User

from .mixins import (CreateListRetrieveDelUpdFovoriteViewSet,
                     CreateListRetrieveViewSet)
from .pagination import PageLimitPagination
from .permissions import AuthForItemOrReadOnly
from .serializers import (CustomSetPasswordSerializer, IngredientSerializer,
                          RecipesPostSerializer, RecipesSerializer,
                          SubscribeSerializer, TagSerializer,
                          UserPostSerializer, UserSerializer)
from .utils import html_to_pdf


class CustomUserViewSet(CreateListRetrieveViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AuthForItemOrReadOnly,)

    def get_serializer_class(self):
        if self.action == 'create':
            return UserPostSerializer
        if self.action in ('subscribe', 'subscriptions'):
            return SubscribeSerializer
        return UserSerializer

    @action(
        detail=False,
        methods=['get'],
        permission_classes=(permissions.IsAuthenticated,),
        url_path='me',
    )
    def me_path(self, request):
        if request.method == 'GET':
            user = request.user
            serializer = UserSerializer(user, context={'request': request})
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        ["post"],
        detail=False,
        permission_classes=(permissions.IsAuthenticated,),
    )
    def set_password(self, request):
        data = request.data
        serializer = CustomSetPasswordSerializer(
            data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.request.user.set_password(request.data["new_password"])
        self.request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=["post", "delete"],
        detail=True,
        permission_classes=(permissions.IsAuthenticated,),
    )
    def subscribe(self, request, id):
        user = request.user
        recipe_author = get_object_or_404(User, id=id)
        if request.method == "POST":
            if Follow.objects.filter(
                    user=user,
                    author=recipe_author).exists() or user == recipe_author:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            Follow.objects.create(user=user, author=recipe_author)
            serializer = SubscribeSerializer(
                recipe_author, context={'request': request})
            return Response(serializer.data)
        if request.method == "DELETE":
            if not Follow.objects.filter(
                    user=user, author=recipe_author).exists():
                return Response(status=status.HTTP_400_BAD_REQUEST)
            Follow.objects.filter(user=user, author=recipe_author).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=["get"],
        detail=False,
        permission_classes=(permissions.IsAuthenticated,),
        pagination_class=PageLimitPagination
    )
    def subscriptions(self, request):
        user = request.user
        recipes_limit = request.GET.get('recipes_limit')
        queryset = self.queryset.filter(following__user=user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={
                                             'request': request,
                                             'recipes_limit': recipes_limit})
            return self.get_paginated_response(serializer.data)
        serializer = SubscribeSerializer(queryset, many=True, context={
                                         'request': request,
                                         'recipes_limit': recipes_limit})
        return Response(serializer.data)


class RecipesViewSet(CreateListRetrieveDelUpdFovoriteViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipesSerializer

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return RecipesSerializer
        return RecipesPostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        ["get"],
        detail=False,
        permission_classes=(permissions.IsAuthenticated,),
    )
    def download_shopping_cart(self, request):
        user = request.user
        users_recipes = Recipe.objects.filter(shopping_cart=user)
        data = Ingredient.objects.filter(
            recipes__in=users_recipes).values(
                'name', 'measurement_unit').annotate(
                    amount=Sum('ingredients_recipe__amount')
        )
        data_dict = {'data': data}
        pdf = html_to_pdf('spisok_template.html', data_dict)
        return HttpResponse(pdf, content_type='application/pdf')


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter)
    search_fields = ('^name',)
    ordering = ('name',)
    #filterset_fields = ('name',)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
