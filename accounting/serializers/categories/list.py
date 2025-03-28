from rest_framework import serializers

from accounting.models.categories import Category


class CategoryListInputSerializer(serializers.Serializer):
    type = serializers.ChoiceField(
        choices=Category.Type.choices,
        default=None,
    )


class CategoryListItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    type = serializers.ChoiceField(choices=Category.Type.choices)
    parent_id = serializers.IntegerField(allow_null=True)
    updated_at = serializers.DateTimeField()
    created_at = serializers.DateTimeField()


class CategoryListOutputSerializer(serializers.Serializer):
    categories = serializers.ListSerializer(child=CategoryListItemSerializer())
