from rest_framework import serializers


class AccountUpdateInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=64)
    is_public = serializers.BooleanField()
    initial_balance = serializers.DecimalField(max_digits=10, decimal_places=2)
