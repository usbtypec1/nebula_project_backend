from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from telegram_auth.use_cases import TelegramAuthenticateUseCase


User = get_user_model()



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
            'access': result.access_token,
            'refresh': result.refresh_token,
        }
        return Response(response_data, status.HTTP_200_OK)
