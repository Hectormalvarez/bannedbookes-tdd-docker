from rest_framework import serializers

from .models import Ban, Book


class BanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ban
        fields = "__all__"
        extra_kwargs = {
            "secondary_author": {
                "required": False,
                "allow_blank": True,
                "allow_null": True,
            },
            "illustrator": {"required": False, "allow_blank": True, "allow_null": True},
            "translator": {"required": False, "allow_blank": True, "allow_null": True},
        }


class BookSerializer(serializers.ModelSerializer):
    bans = BanSerializer(many=True, required=False)

    class Meta:
        model = Book
        fields = ("id", "title", "author", "created_date", "updated_date", "bans")
