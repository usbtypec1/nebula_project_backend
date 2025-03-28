from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from accounting.use_cases import CategoryDeleteUseCase


class CategoryRetrieveUpdateDeleteApi(APIView):

    def get(self, request: Request, category_id: int) -> Response:
        return Response(status=status.HTTP_200_OK)

    def put(self, request: Request, category_id: int) -> Response:
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request: Request, category_id: int) -> Response:
        CategoryDeleteUseCase(
            category_id=category_id,
            user_id=request.user.id,
        ).execute()
        return Response(status=status.HTTP_204_NO_CONTENT)
