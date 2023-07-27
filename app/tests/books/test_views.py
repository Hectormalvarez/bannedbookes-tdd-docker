import json

import pytest

from books.models import Book


@pytest.mark.django_db
def test_add_book(client):
    books = Book.objects.all()
    assert len(books) == 0

    resp = client.post(
        "/api/v1/books/",
        {
            "title": "The Awakening",
            "author": "Kate Chopin"
        },
        content_type="application/json"
    )
    assert resp.status_code == 201
    assert resp.data["title"] == "The Awakening"

    books = Book.objects.all()
    assert len(books) == 1

@pytest.mark.django_db
def test_add_book_invalid_json(client):
    books = Book.objects.all()
    assert len(books) == 0

    resp = client.post(
        "/api/v1/books/",
        {},
        content_type="application/json"
    )
    assert resp.status_code == 400

    books = Book.objects.all()
    assert len(books) == 0

@pytest.mark.django_db
def test_add_book_invalid_json_keys(client):
    books = Book.objects.all()
    assert len(books) == 0

    resp = client.post(
        "/api/v1/books/",
        {
            "title": "The Awakening",
        },
        content_type="application/json"
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