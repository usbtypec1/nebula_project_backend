from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from accounting.serializers import (
    TransactionRetrieveOutputSerializer,
    TransactionUpdateInputSerializer,
)
from accounting.use_cases import (
    TransactionDeleteUseCase,
    TransactionRetrieveUseCase,
    TransactionUpdateUseCase,
)


class TransactionRetrieveUpdateDeleteApi(APIView):

    def get(self, request: Request, transaction_id: int) -> Response:
        transaction = TransactionRetrieveUseCase(
            transaction_id=transaction_id,
            user_id=request.user.id,
        ).execute()

        serializer = TransactionRetrieveOutputSerializer(transaction)
        return Response(serializer.data)

    def put(self, request: Request, transaction_id: int) -> Response:
        serializer = TransactionUpdateInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data: dict = serializer.validated_data

        TransactionUpdateUseCase(
            transaction_id=transaction_id,
            user_id=request.user.id,
            description=data["description"],
            amount=data["amount"],
            date=data["date"],
        ).execute()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request: Request, transaction_id: int) -> Response:
        TransactionDeleteUseCase(
            transaction_id=transaction_id,
            user_id=request.user.id,
        ).execute()
        return Response(status=status.HTTP_204_NO_CONTENT)
