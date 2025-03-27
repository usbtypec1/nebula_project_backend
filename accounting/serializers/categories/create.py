from rest_framework import serializers

from accounting.models.categories import Category


class CategoryCreateInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=64, min_length=1)
    parent_id = serializers.IntegerField(allow_null=True, default=None)
    type = serializers.ChoiceField(choices=Category.Type.choices)


class CategoryCreateOutputSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    parent_id = serializers.IntegerField(allow_null=True)
    type = serializers.ChoiceField(choices=Category.Type.choices)
    updated_at = serializers.DateTimeField()
    created_at = serializers.DateTimeField()
