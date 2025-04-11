from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from accounting.serializers import (
    TransferCreateInputSerializer,
    TransferCreateOutputSerializer,
    TransferListInputSerializer,
    TransferListOutputSerializer,
)
from accounting.use_cases import TransferCreateUseCase, TransferListUseCase


class TransferListCreateApi(APIView):

    def get(self, request: Request) -> Response:
        serializer = TransferListInputSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        data: dict = serializer.validated_data

        transfers_page = TransferListUseCase(
            user_id=request.user.id,
            take=data['take'],
            skip=data['skip'],
        ).execute()

        serializer = TransferListOutputSerializer(transfers_page)
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        serializer = TransferCreateInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data: dict = serializer.validated_data

        transfer = TransferCreateUseCase(
            description=data['description'],
            from_account_id=data['from_account_id'],
            to_account_id=data['to_account_id'],
            amount=data['amount'],
            date=data['date'],
        ).execute()

        serializer = TransferCreateOutputSerializer(transfer)
        return Response(serializer.data)
