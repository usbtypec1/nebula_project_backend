from django.conf import settings
from django.urls import path
from .views import TelegramAuthView


urlpatterns = [
    path(
        'token/', TelegramAuthView.as_view(),
        name='token_obtain_telegram',
    ),
]

if settings.DEBUG:
    from .views import TelegramAuthTestApi

    urlpatterns.append(
        path(
            'test-token/', TelegramAuthTestApi.as_view(),
            name='test_telegram_auth',
        )
    )
