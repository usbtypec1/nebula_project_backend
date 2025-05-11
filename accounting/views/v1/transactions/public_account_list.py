from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from accounting.serializers import TransactionListOutputSerializer
from accounting.use_cases import PublicAccountTransactionListUseCase


class PublicAccountTransactionListApi(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request: Request, account_id: int) -> Response:
        transactions_page = (
            PublicAccountTransactionListUseCase(account_id=account_id)
            .execute()
        )
        serializer = TransactionListOutputSerializer(transactions_page)
        return Response(serializer.data)
