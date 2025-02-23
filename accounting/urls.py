from django.urls import path

from accounting.views import AccountListApi


app_name = 'accounting'
urlpatterns = [
    path('accounts/', AccountListApi.as_view(), name='account-list'),
]
