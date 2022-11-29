from django.urls import include, path

from .routers import router_v1

app_name = 'api'

urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
