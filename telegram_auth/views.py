from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from telegram_auth.services import TelegramAuthenticateInteractor


class TelegramAuthView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        response_data = TelegramAuthenticateInteractor(
            request_data=request.data,
            ttl_in_seconds=3600 * 24,
            bot_token=settings.TELEGRAM_BOT_TOKEN,
        ).execute()
        return Response(response_data, status=status.HTTP_200_OK)
