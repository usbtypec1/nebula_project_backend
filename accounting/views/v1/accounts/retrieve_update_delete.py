from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from accounting.serializers import AccountRetrieveOutputSerializer
from accounting.use_cases import AccountDeleteUseCase, AccountRetrieveUseCase


class AccountRetrieveUpdateDeleteApi(APIView):

    def get(self, request: Request, account_id: int) -> Response:
        account = AccountRetrieveUseCase(
            account_id=account_id,
            user_id=request.user.id,
        ).execute()
        serializer = AccountRetrieveOutputSerializer(account)
        return Response(serializer.data, status.HTTP_200_OK)

    def put(self, request: Request, account_id: int) -> Response:
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request: Request, account_id: int) -> Response:
        AccountDeleteUseCase(
            account_id=account_id,
            user_id=request.user.id,
        ).execute()
        return Response(status=status.HTTP_204_NO_CONTENT)
