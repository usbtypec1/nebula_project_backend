from rest_framework import serializers


class TransferUpdateInputSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    description = serializers.CharField(
        max_length=1024,
        allow_null=True,
        default=None,
    )
    date = serializers.DateTimeField()
