from rest_framework import serializers

from accounting.models import Category


class TransactionCreateInputSerializer(serializers.Serializer):
    account_id = serializers.IntegerField()
    category_id = serializers.IntegerField()
    date = serializers.DateTimeField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    description = serializers.CharField(allow_null=True)


class TransactionCreateOutputSerializer(serializers.Serializer):
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
