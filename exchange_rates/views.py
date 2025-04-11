from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from exchange_rates.serializers import ExchangeRateListOutputSerializer
from exchange_rates.use_cases.exchange_rate_list import ExchangeRateListUseCase


class ExchangeRateListApi(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request: Request) -> Response:
        exchange_rates = ExchangeRateListUseCase().execute()

        serializer = ExchangeRateListOutputSerializer(
            exchange_rates,
            many=True,
        )
        return Response({'exchange_rates': serializer.data})
