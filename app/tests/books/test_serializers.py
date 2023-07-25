from books.serializers import BookSerializer


def test_valid_movie_serializer():
    valid_serializer_data = {
        "title": "harry potter",
        "author": "JK Rowling",
    }
    serializer = BookSerializer(data=valid_serializer_data)
    assert serializer.is_valid()
    assert serializer.validated_data == valid_serializer_data
    assert serializer.data == valid_serializer_data
    assert serializer.errors == {}

def test_invalid_movie_serializer():
    invalid_serializer_data = {
        "title": "harry potter",
    }
    serializer = BookSerializer(data=invalid_serializer_data)
    assert not serializer.is_valid()
    assert serializer.validated_data == {}
    assert serializer.data == invalid_serializer_data
    assert serializer.errors == {"author": ["This field is required."]}