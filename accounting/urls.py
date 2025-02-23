from django.urls import include, path

from accounting.views import (
    CategoryListCreateApi,
    CategoryRetrieveUpdateDeleteApi,
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

urlpatterns = [
    path('v1/categories/', include(categories_urlpatterns)),
]
