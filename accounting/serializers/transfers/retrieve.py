from rest_framework import serializers


class TransferRetrieveOutputSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    from_account_id = serializers.IntegerField()
    from_account_name = serializers.CharField()
    to_account_id = serializers.IntegerField()
    to_account_name = serializers.CharField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    description = serializers.CharField(allow_null=True)
    date = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    created_at = serializers.DateTimeField()
