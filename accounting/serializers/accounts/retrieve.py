from rest_framework import serializers


class AccountRetrieveOutputSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    initial_balance = serializers.DecimalField(max_digits=10, decimal_places=2)
    is_public = serializers.BooleanField()
    balance = serializers.DecimalField(max_digits=10, decimal_places=2)
    created_at = serializers.DateTimeField()
