from rest_framework import serializers


class AccountCreateInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=64)
    is_public = serializers.BooleanField()
    initial_balance = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )


class AccountCreateOutputSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    is_public = serializers.BooleanField()
    initial_balance = serializers.DecimalField(max_digits=10, decimal_places=2)
    created_at = serializers.DateTimeField()
