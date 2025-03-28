from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from accounting.serializers.categories.create import (
    CategoryCreateInputSerializer,
    CategoryCreateOutputSerializer,
)
from accounting.serializers.categories.list import (
    CategoryListInputSerializer,
    CategoryListOutputSerializer,
)
from accounting.use_cases import CategoryCreateUseCase
from accounting.use_cases.category_list import CategoryListUseCase


class CategoryListCreateApi(APIView):

    def get(self, request: Request) -> Response:
        serializer = CategoryListInputSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        category_type: int | None = serializer.validated_data['type']

        category_list_result = CategoryListUseCase(
            user_id=request.user.id,
            category_type=category_type,
        ).execute()

        serializer = CategoryListOutputSerializer(category_list_result)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        serializer = CategoryCreateInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        name: str = serializer.validated_data['name']
        parent_id: int | None = serializer.validated_data['parent_id']
        category_type: int = serializer.validated_data['type']

        category_create_result = CategoryCreateUseCase(
            name=name,
            parent_id=parent_id,
            user_id=request.user.id,
            type=category_type,
        ).execute()

        serializer = CategoryCreateOutputSerializer(category_create_result)
        return Response(serializer.data, status.HTTP_201_CREATED)
