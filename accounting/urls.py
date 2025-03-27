from django.urls import include, path

from accounting.views import (
    AccountListCreateApi,
    CategoryRetrieveUpdateDeleteApi,
    CategoryListCreateApi,
)


app_name = 'accounting'

categories_urlpatterns = [
    path(
        '',
        CategoryListCreateApi.as_view(),
        name='category-list-create',
    ),
    path(
        '<int:category_id>/',
        CategoryRetrieveUpdateDeleteApi.as_view(),
        name='category-retrieve-update-delete',
    ),
]

accounts_urlpatterns = [
    path(
        '',
        AccountListCreateApi.as_view(),
        name='account-list-create',
    ),
    path(
        '<int:account_id>/',
        CategoryRetrieveUpdateDeleteApi.as_view(),
        name='account-retrieve-update-delete',
    )
]

urlpatterns = [
    path('categories/', include(categories_urlpatterns)),
    path('accounts/', include(accounts_urlpatterns)),
]
