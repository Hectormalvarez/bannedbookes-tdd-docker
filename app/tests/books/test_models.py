import pytest

from books.models import Book, Ban


@pytest.mark.django_db
def test_book_model():
    book = Book(title="Me and Earl and the Dying Girl", author="Andrews, Jesse")
    book.save()
    assert book.title == "Me and Earl and the Dying Girl"
    assert book.author == "Andrews, Jesse"
    assert book.created_date
    assert book.updated_date
    assert str(book) == book.title


@pytest.mark.django_db
def test_ban_model():
    book = Book(title="Me and Earl and the Dying Girl", author="Andrews, Jesse")
    book.save()
    ban = Ban(
        book=book,
        type_of_ban="Banned in Libraries and Classrooms",
        state="Florida",
        district="Indian River County School District",
        date_of_challenge_removal="November 2021",
        origin_of_challenge="Administrator"
    )
    assert ban.book == book
    assert ban.type_of_ban == "Banned in Libraries and Classrooms"
    assert ban.state == "Florida"
    assert ban.district == "Indian River County School District"
