from rest_framework import serializers


class TransferCreateInputSerializer(serializers.Serializer):
    from_account_id = serializers.IntegerField()
    to_account_id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    description = serializers.CharField(
        max_length=1024,
        allow_null=True,
        default=None,
    )
    date = serializers.DateTimeField()


class TransferCreateOutputSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    from_account_id = serializers.IntegerField()
    to_account_id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    description = serializers.CharField(allow_null=True)
    date = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    created_at = serializers.DateTimeField()
