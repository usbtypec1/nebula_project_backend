from django.urls import path
from .views import TelegramAuthView


urlpatterns = [
    path(
        'token/', TelegramAuthView.as_view(),
        name='token_obtain_telegram'
    ),
]
