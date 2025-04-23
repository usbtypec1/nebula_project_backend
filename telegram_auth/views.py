from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenRefreshView

from telegram_auth.serializers import CookieTokenRefreshSerializer
from telegram_auth.use_cases import TelegramAuthenticateUseCase


User = get_user_model()


class CookieTokenRefreshApi(TokenRefreshView):
    serializer_class = CookieTokenRefreshSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get('refresh'):
            cookie_max_age = 3600 * 24 * 14  # 14 days
            response.set_cookie(
                'refresh_token', response.data['refresh'],
                max_age=cookie_max_age, httponly=True
            )
            del response.data['refresh']
        return super().finalize_response(request, response, *args, **kwargs)


class TelegramAuthApi(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        result = TelegramAuthenticateUseCase(
            request_data=request.data,
            ttl_in_seconds=3600 * 24,
            bot_token=settings.TELEGRAM_BOT_TOKEN,
        ).execute()
        response_data = {
            'access_token': result.access_token,
            'refresh_token': result.refresh_token,
        }
        return Response(response_data, status.HTTP_200_OK)
