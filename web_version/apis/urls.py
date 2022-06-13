from django.urls import path
from .views import status_global


urlpatterns = [
    path('status/global', status_global, name='api_status_global'),
]