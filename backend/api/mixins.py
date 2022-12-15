from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from recipes.models import Recipe
from .filters import RecipeFilter
from .pagination import PageLimitPagination
from .permissions import AuthorOrAuthOrReadOnly
from .serializers import RecipesSubscribeSerializer


class CreateListRetrieveViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    pagination_class = PageLimitPagination
    lookup_field = 'id'


class CreateListRetrieveDelUpdFovoriteViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    pagination_class = PageLimitPagination
    permission_classes = (AuthorOrAuthOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    lookup_field = 'id'

    def get_favorite(self, request, id, related_name):
        user = request.user
        recipe = get_object_or_404(Recipe, id=id)
        recipes_user = getattr(recipe, related_name)
        if request.method == "POST":
            if recipes_user.filter(id=user.id).exists():
                return Response(status=status.HTTP_400_BAD_REQUEST)
            recipes_user.add(user)
            serializer = RecipesSubscribeSerializer(
                recipe, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == "DELETE":
            if not recipes_user.filter(id=user.id).exists():
                return Response(status=status.HTTP_400_BAD_REQUEST)
            recipes_user.remove(user)
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=["post", "delete"],
        detail=True,
        permission_classes=(permissions.IsAuthenticated,),
    )
    def favorite(self, request, id):
        return CreateListRetrieveDelUpdFovoriteViewSet.get_favorite(
            self, request, id, related_name='favorited')

    @action(
        methods=["post", "delete"],
        detail=True,
        permission_classes=(permissions.IsAuthenticated,),
    )
    def shopping_cart(self, request, id):
        return CreateListRetrieveDelUpdFovoriteViewSet.get_favorite(
            self, request, id, related_name='shopping_cart')
