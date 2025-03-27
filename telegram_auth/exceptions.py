from typing import Any

from django.utils.translation import gettext_lazy as _
from drf_standardized_errors.formatter import (
    ExceptionFormatter as BaseExceptionFormatter,
)
from drf_standardized_errors.types import ErrorResponse
from rest_framework.exceptions import APIException
from rest_framework import status


class ExceptionFormatter(BaseExceptionFormatter):

    def format_error_response(self, error_response: ErrorResponse) -> Any:
        extra: dict | None = getattr(self.exc, 'extra', None)

        error_response = super().format_error_response(error_response)
        for error in error_response['errors']:
            if extra is not None and error['code'] == self.exc.default_code:
                error['extra'] = extra
            if error['attr'] is None:
                del error['attr']

        return error_response


class TelegramMiniAppInitDataExpiredError(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_code = 'telegram_mini_app_init_data_expired'
    default_detail = _('Telegram Mini App init data is expired')


class TelegramMiniAppInitDataInvalidError(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_code = 'telegram_mini_app_init_data_invalid'
    default_detail = _('Telegram Mini App init data is invalid')


class TelegramMiniAppInitDataRequiredError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'telegram_mini_app_init_data_required'
    default_detail = _('Telegram Mini App init data is required')


class UserNotFoundError(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_code = 'user_not_found'
    default_detail = _('User not found')
