from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from accounting.serializers import (
    TransferRetrieveOutputSerializer,
    TransferUpdateInputSerializer,
)
from accounting.use_cases import (
    TransferDeleteUseCase,
    TransferRetrieveUseCase,
    TransferUpdateUseCase,
)


class TransferRetrieveUpdateDeleteApi(APIView):

    def get(self, request: Request, transfer_id: int) -> Response:
        transfer = TransferRetrieveUseCase(
            transfer_id=transfer_id,
            user_id=request.user.id,
        ).execute()

        serializer = TransferRetrieveOutputSerializer(transfer)
        return Response(serializer.date)

    def put(self, request: Request, transfer_id: int) -> Response:
        serializer = TransferUpdateInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data: dict = serializer.validated_data

        TransferUpdateUseCase(
            transfer_id=transfer_id,
            user_id=request.user.id,
            date=data['date'],
            description=data['dsecription'],
            amount=data['amount'],
        ).execute()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request: Request, transfer_id: int) -> Response:
        TransferDeleteUseCase(
            transfer_id=transfer_id,
            user_id=request.user.id,
        ).execute()
        return Response(status=status.HTTP_204_NO_CONTENT)
