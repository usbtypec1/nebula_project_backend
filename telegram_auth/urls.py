from django.urls import path

from telegram_auth.views import CookieTokenRefreshApi, TelegramAuthApi, TelegramAuthTestApi


urlpatterns = [
    path(
        'token/',
        TelegramAuthApi.as_view(),
        name='token-obtain',
    ),
    path(
        'token/test',
        TelegramAuthTestApi.as_view(),
    ),
    path(
        'token/refresh/',
        CookieTokenRefreshApi.as_view(),
        name='token-refresh',
    ),
]
