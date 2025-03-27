from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

from telegram_auth.services import TelegramAuthenticateInteractor


User = get_user_model()


class CookieTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = None

    def validate(self, attrs):
        attrs['refresh'] = self.context['request'].COOKIES.get('refresh_token')
        if attrs['refresh']:
            return super().validate(attrs)
        else:
            raise InvalidToken(
                'No valid token found in cookie \'refresh_token\''
            )


class CookieTokenRefreshView(TokenRefreshView):
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


class TelegramAuthTestApi(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request: Request) -> Response:
        user = User.objects.get(
            telegram_id=request.query_params['telegram_id']
        )
        token = RefreshToken.for_user(user)
        response = Response()
        response.set_cookie(
            'access_token',
            str(token.access_token),
            httponly=True,
            samesite='Lax',
            expires=token.access_token.get('exp'),
        )
        response.set_cookie(
            'refresh_token',
            str(token),
            httponly=True,
            samesite='Lax',
            expires=token.get('exp'),
        )
        return response
