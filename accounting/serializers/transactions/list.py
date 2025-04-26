from rest_framework import serializers

from accounting.models import Category


class TransactionListInputSerializer(serializers.Serializer):
    take = serializers.IntegerField(default=100, min_value=1)
    skip = serializers.IntegerField(default=0, min_value=0)
    from_date = serializers.DateTimeField(default=None)
    to_date = serializers.DateTimeField(default=None)
    category_type = serializers.ChoiceField(
        choices=Category.Type.choices,
        default=None,
    )


class TransactionListItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    account_id = serializers.IntegerField()
    account_name = serializers.CharField()
    category_id = serializers.IntegerField()
    category_type = serializers.ChoiceField(choices=Category.Type.choices)
    category_name = serializers.CharField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    description = serializers.CharField(allow_null=True)
    date = serializers.DateTimeField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class PaginationSerializer(serializers.Serializer):
    taken_count = serializers.IntegerField()
    skipped_count = serializers.IntegerField()
    total_count = serializers.IntegerField()


class TransactionListOutputSerializer(serializers.Serializer):
    transactions = TransactionListItemSerializer(many=True)
    pagination = PaginationSerializer()
