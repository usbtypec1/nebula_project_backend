from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class TransferRetrieveUpdateDeleteApi(APIView):

    def get(self, request: Request, transfer_id: int) -> Response:
        return Response()

    def put(self, request: Request, transfer_id: int) -> Response:
        return Response()

    def delete(self, request: Request, transfer_id: int) -> Response:
        return Response()
