import pytest

from books.models import Book


@pytest.mark.django_db
def test_book_model():
    book = Book(title="Me and Earl and the Dying Girl", author="Andrews, Jesse")
    book.save()
    assert book.title == "Me and Earl and the Dying Girl"
    assert book.author == "Andrews, Jesse"
    assert book.created_date
    assert book.updated_date
    assert str(book) == book.title
