import json
import requests
from pen_america_bannedbooks_scraper import get_data

# Define the API base URL and endpoint for adding bans and books
base_url = "http://localhost:8009/api/v1/"
book_endpoint = "books/"
ban_endpoint = "bans/"

def main():
    # Seed data in JSON format
    with open('app/scripts/banned_books.json') as f:
        seed_data = json.load(f)

    # seed_data = get_data()
    print("seed data downloaded, proceeding with database loading")
    upload_books_with_bans(seed_data)

def create_book(book_data):
    # Make a POST request to create the book
    response = requests.post(f"{base_url}{book_endpoint}", json=book_data)
    if response.status_code == 201:
        return response.json()["id"]
    else:
        print(f"Failed to create book. Status Code: {response.status_code}")
        return None

def create_book_and_bans(book_data, bans):
    book_id = create_book(book_data)
    if book_id is not None:
        # Make a POST request for each ban to create bans for this book
        for ban_data in bans:
            ban_data["book"] = book_id
            response = requests.post(
                f"{base_url}{book_endpoint}{book_id}/{ban_endpoint}", json=ban_data
            )
            if response.status_code == 201:
                print(f"Ban created successfully for Book ID {book_id}")
            else:
                print(
                    f"Failed to create ban for Book ID {book_id}. Status Code: {response.status_code}"
                )

def upload_books_with_bans(data):
    # Upload seed data to the API
    response = requests.post(f"{base_url}{book_endpoint}", json=data)
    if response.status_code == 201:
        print("Seed data uploaded successfully")
    else:
        print(f"Failed to upload seed data. Status Code: {response.status_code}")

# Create bans for each book in the seed data


# for book_data in seed_data[:1]:
#     bans = book_data["bans"]
#     print(book_data)
#     # Fetch the Book instance based on title and author (Assuming you have a view to search books)
#     book_search_url = f"{base_url}{book_endpoint}/search?title={book_data['title']}"
#     response = requests.get(book_search_url)

#     if response.status_code == 200:
#         book_data_response = response.json()
#         if book_data_response and isinstance(book_data_response, list):
#             # Book exists, use the first match
#             book_id = book_data_response[0]["id"]
#             create_book_and_bans({"id": book_id}, bans)
#         else:
#             # Book does not exist, create the book and its bans
#             create_book_and_bans(book_data, bans)
#     elif response.status_code == 404:
#         # Book not found, create the book and its bans
#         create_book_and_bans(book_data, bans)
#     else:
#         print(response)
#         print(f"Failed to fetch book. Status Code: {response.status_code}")


if __name__ == "__main__":
    main()
