from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException


class AccountAlreadyExistsError(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_code = 'account_already_exists'
    default_detail = _('Account already exists')


class AccountAccessDeniedError(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_code = 'account_access_denied'
    default_detail = _('Access denied to account')


class AccountNotFoundError(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_code = 'account_not_found'
    default_detail = _('Account not found')
