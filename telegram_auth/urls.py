from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from telegram_auth.views import TelegramAuthApi


urlpatterns = [
    path(
        'token/',
        TelegramAuthApi.as_view(),
        name='token-obtain',
    ),
    path(
        'token/refresh/',
        TokenRefreshView.as_view(),
        name='token-refresh',
    ),
]
