from rest_framework import serializers


class AccountListItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    is_public = serializers.BooleanField()
    initial_balance = serializers.DecimalField(max_digits=10, decimal_places=2)
    balance = serializers.DecimalField(max_digits=10, decimal_places=2)
    created_at = serializers.DateTimeField()


class AccountListOutputSerializer(serializers.Serializer):
    accounts = serializers.ListField(child=AccountListItemSerializer())
    total_balance = serializers.DecimalField(max_digits=10, decimal_places=2)
