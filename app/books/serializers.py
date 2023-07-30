from rest_framework import serializers

from .models import Ban, Book


class BookSerializer(serializers.ModelSerializer):
    bans = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ("id", "title", "author", "created_date", "updated_date", "bans")


class BanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ban
        fields = "__all__"
