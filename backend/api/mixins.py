from rest_framework import mixins, viewsets

from .pagination import PageLimitPagination


class CreateListRetrieveViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    pagination_class = PageLimitPagination
    lookup_field = 'id'
