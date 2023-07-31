import pytest
from rest_framework.test import APIClient

from books.models import Ban, Book


@pytest.mark.django_db
def test_add_book(client):
    books = Book.objects.all()
    assert len(books) == 0

    resp = client.post(
        "/api/v1/books/",
        [{"title": "The Awakening", "author": "Kate Chopin"}],
        content_type="application/json",
    )
    assert resp.status_code == 201
    assert resp.data["title"] == "The Awakening"

    books = Book.objects.all()
    assert len(books) == 1


@pytest.mark.django_db
def test_add_book_invalid_json(client):
    books = Book.objects.all()
    assert len(books) == 0

    resp = client.post("/api/v1/books/", [{}], content_type="application/json")
    assert resp.status_code == 400

    books = Book.objects.all()
    assert len(books) == 0


@pytest.mark.django_db
def test_add_book_invalid_json_keys(client):
    books = Book.objects.all()
    assert len(books) == 0

    resp = client.post(
        "/api/v1/books/",
        [
            {
                "title": "The Awakening",
            }
        ],
        content_type="application/json",
    )
    assert resp.status_code == 400

    books = Book.objects.all()
    assert len(books) == 0


@pytest.mark.django_db
def test_get_single_book(client, add_book):
    book = add_book(title="The Awakening", author="Kate Chopin")
    resp = client.get(f"/api/v1/books/{book.id}/")
    assert resp.status_code == 200
    assert resp.data["title"] == "The Awakening"


def test_get_single_book_incorrect_id(client):
    resp = client.get("/api/v1/books/foo/")
    assert resp.status_code == 404


@pytest.mark.django_db
def test_get_all_books(client, add_book):
    book_one = add_book(title="The Awakening", author="Kate Chopin")
    book_two = add_book("City of Glass", "Paul Auster")
    resp = client.get("/api/v1/books/")
    assert resp.status_code == 200
    assert resp.data[0]["title"] == book_one.title
    assert resp.data[1]["title"] == book_two.title


# @pytest.mark.django_db
# def test_add_book_ban(client, add_book):
#     ban = Ban.objects.all()
#     assert len(ban) == 0

#     book = add_book(title="The Awakening", author="Kate Chopin")
#     resp = client.post(
#         f"/api/v1/bans/",
#         [
#             {
#                 "book": book.id,
#                 "type_of_ban": "Banned in schools",
#                 "secondary_author": "",
#                 "illustrator": "",
#                 "translator": "",
#                 "state": "New York",
#                 "district": "Manhattan",
#                 "date_of_challenge_removal": "9/2021",
#                 "origin_of_challenge": "Parents group",
#             },
#         ],
#         content_type="application/json",
#     )
#     print(resp)
#     assert resp.status_code == 201

#     ban = Ban.objects.all()
#     assert len(ban) == 1


@pytest.mark.django_db
def test_add_book_with_bans():
    client = APIClient()

    book_with_bans = [
        {
            "title": "The Poet X",
            "author": "Elizabeth Acevedo",
            "bans": [
                {
                    "type_of_ban": "Banned Pending Investigation",
                    "state": "Texas",
                    "district": "Fredericksburg Independent School District",
                    "date_of_challenge_removal": "March 2022",
                    "origin_of_challenge": "Administrator",
                },
                {
                    "type_of_ban": "Banned in Libraries",
                    "state": "Virginia",
                    "district": "New Kent County Public Schools",
                    "date_of_challenge_removal": "October 2021",
                    "origin_of_challenge": "Administrator",
                },
            ],
        }
    ]

    resp = client.post(
        "/api/v1/books/",
        book_with_bans,
        format="json",  # Use 'format="json"' instead of 'content_type="application/json"'
    )
    print(resp.data)
    assert resp.status_code == 201
