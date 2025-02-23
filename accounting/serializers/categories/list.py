from rest_framework import serializers

from accounting.models.categories import Category


class CategoryListInputSerializer(serializers.Serializer):
    take = serializers.IntegerField(min_value=1, max_value=1000, default=100)
    skip = serializers.IntegerField(min_value=0, default=0)
    type = serializers.ChoiceField(
        choices=Category.Type.choices,
        default=None,
    )


class CategoryListItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    parent_id = serializers.IntegerField(allow_null=True)
    updated_at = serializers.DateTimeField()
    created_at = serializers.DateTimeField()


class CategoryListOutputSerializer(serializers.Serializer):
    categories = serializers.ListSerializer(child=CategoryListItemSerializer())
    is_end_of_list_reached = serializers.BooleanField()
