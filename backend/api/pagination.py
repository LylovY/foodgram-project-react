from rest_framework.pagination import PageNumberPagination


class PageLimitPagination(PageNumberPagination):
    page_query_param = "page"   # this is the "page"
    page_size_query_param = "limit" # this is the "page_size"
    #page_size = 5
    max_page_size = 100
