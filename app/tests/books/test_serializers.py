import pytest
from books.models import Book
from books.serializers import BookSerializer, BanSerializer


@pytest.mark.django_db
def test_valid_book_serializer():
    valid_serializer_data = {
        "title": "harry potter",
        "author": "JK Rowling",
    }
    serializer = BookSerializer(data=valid_serializer_data)
    assert serializer.is_valid()
    assert serializer.validated_data == valid_serializer_data
    assert serializer.data == valid_serializer_data
    assert serializer.errors == {}


@pytest.mark.django_db
def test_invalid_book_serializer():
    invalid_serializer_data = {
        "title": "harry potter",
    }
    serializer = BookSerializer(data=invalid_serializer_data)
    assert not serializer.is_valid()
    assert serializer.validated_data == {}
    assert serializer.data == invalid_serializer_data
    assert serializer.errors == {"author": ["This field is required."]}


@pytest.mark.django_db
def test_valid_ban_serializer():
    # Create a Book instance to be associated with the Ban
    book_data = {
        "title": "The Catcher in the Rye",
        "author": "J.D. Salinger",
    }
    book = Book.objects.create(**book_data)

    valid_serializer_data = {
        "book": book.id,
        "type_of_ban": "Banned in schools",
        "secondary_author": "",
        "illustrator": "",
        "translator": "",
        "state": "New York",
        "district": "Manhattan",
        "date_of_challenge_removal": "November 2022",
        "origin_of_challenge": "Parents group",
    }

    serializer = BanSerializer(data=valid_serializer_data)
    assert serializer.is_valid()

    # Manually update valid_serializer_data with the nested Book instance
    valid_serializer_data["book"] = book

    assert serializer.validated_data == valid_serializer_data
    assert serializer.errors == {}


@pytest.mark.django_db
def test_invalid_ban_serializer():
    invalid_serializer_data = {
        "type_of_ban": "Banned in schools",
        "state": "New York",
        "district": "Manhattan",
        "date_of_challenge_removal": "September 2022",
        "origin_of_challenge": "Parents group",
    }

    serializer = BanSerializer(data=invalid_serializer_data)
    assert not serializer.is_valid()
    assert serializer.validated_data == {}
    assert serializer.errors == {"book": ["This field is required."]}
