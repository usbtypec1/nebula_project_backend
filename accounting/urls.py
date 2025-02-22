from django.urls import path
from rest_framework.urls import app_name

from accounting.views import AccountListApi


app_name = 'accounting'
urlpatterns = [
    path('accounts/', AccountListApi.as_view(), name='account-list'),
]
