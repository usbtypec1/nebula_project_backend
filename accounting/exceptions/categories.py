from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException


class CategoryNotFoundError(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_code = 'category_not_found'
    default_detail = _('Category not found')


class CategoryAlreadyExistsError(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_code = 'category_already_exists'
    default_detail = _('Category already exists')
