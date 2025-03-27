from decimal import Decimal

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from accounting.serializers import (
    AccountCreateInputSerializer,
    AccountCreateOutputSerializer,
)
from accounting.use_cases import AccountCreateUseCase


class AccountListCreateApi(APIView):

    def get(self, request: Request) -> Response:
        pass

    def post(self, request: Request) -> Response:
        serializer = AccountCreateInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data: dict = serializer.validated_data
        name: str = validated_data['name']
        is_public: bool = validated_data['is_public']
        initial_balance: Decimal = validated_data['initial_balance']

        category_create_result = AccountCreateUseCase(
            name=name,
            user_id=request.user.id,
            is_public=is_public,
            initial_balance=initial_balance,
        ).execute()

        serializer = AccountCreateOutputSerializer(category_create_result)
        return Response(serializer.data, status.HTTP_201_CREATED)
