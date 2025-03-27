from decimal import Decimal

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from accounting.serializers import AccountRetrieveOutputSerializer
from accounting.serializers.accounts import AccountUpdateInputSerializer
from accounting.use_cases import (
    AccountDeleteUseCase,
    AccountRetrieveUseCase,
    AccountUpdateUseCase,
)


class AccountRetrieveUpdateDeleteApi(APIView):

    def get(self, request: Request, account_id: int) -> Response:
        account = AccountRetrieveUseCase(
            account_id=account_id,
            user_id=request.user.id,
        ).execute()
        serializer = AccountRetrieveOutputSerializer(account)
        return Response(serializer.data, status.HTTP_200_OK)

    def put(self, request: Request, account_id: int) -> Response:
        serializer = AccountUpdateInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data: dict = serializer.validated_data
        name: str = validated_data['name']
        is_public: bool = validated_data['is_public']
        initial_balance: Decimal = validated_data['initial_balance']

        AccountUpdateUseCase(
            account_id=account_id,
            user_id=request.user.id,
            name=name,
            is_public=is_public,
            initial_balance=initial_balance,
        ).execute()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request: Request, account_id: int) -> Response:
        AccountDeleteUseCase(
            account_id=account_id,
            user_id=request.user.id,
        ).execute()
        return Response(status=status.HTTP_204_NO_CONTENT)
