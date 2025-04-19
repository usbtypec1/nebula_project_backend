from rest_framework import serializers


class TransferListInputSerializer(serializers.Serializer):
    take = serializers.IntegerField(default=100, min_value=1)
    skip = serializers.IntegerField(default=0, min_value=0)


class TransferListItemSerializer(serializers.Serializer):
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


class PaginationSerializer(serializers.Serializer):
    taken_count = serializers.IntegerField()
    skipped_count = serializers.IntegerField()
    total_count = serializers.IntegerField()


class TransferListOutputSerializer(serializers.Serializer):
    transfers = TransferListItemSerializer(many=True)
    pagination = PaginationSerializer()
