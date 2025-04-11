from rest_framework.exceptions import APIException
from rest_framework import status
from django.utils.translation import gettext_lazy as _


class TransactionAccessDeniedError(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_code = "transaction_access_denied"
    default_detail = _(
        "You do not have permission to access this transaction."
    )


class TransactionNotFoundError(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_code = "transaction_not_found"
    default_detail = _("Transaction not found.")
