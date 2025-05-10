from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from accounting.serializers import AccountRetrieveOutputSerializer
from accounting.use_cases import PublicAccountRetrieveUseCase


class PublicAccountRetrieveApi(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request: Request, account_id: int) -> Response:
        account = PublicAccountRetrieveUseCase(account_id=account_id).execute()
        serializer = AccountRetrieveOutputSerializer(account)
        return Response(serializer.data)
