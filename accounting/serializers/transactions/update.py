from rest_framework import serializers


class TransactionUpdateInputSerializer(serializers.Serializer):
    date = serializers.DateTimeField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    description = serializers.CharField(allow_null=True)
