from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from accounting.serializers import (
    TransactionCreateInputSerializer, TransactionCreateOutputSerializer,
    TransactionListInputSerializer,
    TransactionListOutputSerializer,
)
from accounting.use_cases import (
    TransactionCreateUseCase,
    TransactionListUseCase,
)


class TransactionListCreateApi(APIView):

    def get(self, request: Request) -> Response:
        serializer = TransactionListInputSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        data: dict = serializer.validated_data

        transactions_page = TransactionListUseCase(
            take=data['take'],
            skip=data['skip'],
        ).execute()
        serializer = TransactionListOutputSerializer(transactions_page)
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        serializer = TransactionCreateInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data: dict = serializer.validated_data

        transaction = TransactionCreateUseCase(
            user_id=request.user.id,
            description=data['description'],
            amount=data['amount'],
            date=data['date'],
            category_id=data['category_id'],
            account_id=data['account_id'],
        ).execute()

        serializer = TransactionCreateOutputSerializer(transaction)
        return Response(serializer.data, status.HTTP_201_CREATED)
