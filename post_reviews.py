
import requests
from collections import defaultdict

BASE_URL = "http://localhost:4004/odata/v4/catalog"

# Get available books
response = requests.get(f"{BASE_URL}/Books")
response.raise_for_status()
books = response.json()["value"]

if not books:
    raise RuntimeError("No books found in the CAP service.")

# Prepare three reviews for the available books
reviews_to_post = [
    {
        "rating": 5,
        "comment": "Excellent book!",
        "book_ID": books[0]["ID"],
    },
    {
        "rating": 4,
        "comment": "Very informative.",
        "book_ID": books[0]["ID"],
    },
    {
        "rating": 3,
        "comment": "Good, but could be better.",
        "book_ID": books[1]["ID"] if len(books) > 1 else books[0]["ID"],
    },
]

# Post each review
for review in reviews_to_post:
    response = requests.post(
        f"{BASE_URL}/Reviews",
        json=review,
    )

    if response.status_code not in (200, 201):
        print("Failed to post review:", response.status_code, response.text)
        response.raise_for_status()

    print(f"Posted review with rating {review['rating']}")

# Retrieve all reviews
response = requests.get(f"{BASE_URL}/Reviews")
response.raise_for_status()
reviews = response.json()["value"]

# Calculate average rating per book
ratings_by_book = defaultdict(list)

for review in reviews:
    ratings_by_book[review["book_ID"]].append(review["rating"])

book_titles = {book["ID"]: book["title"] for book in books}

print("\nAverage rating per book:")

for book_id, ratings in ratings_by_book.items():
    average = sum(ratings) / len(ratings)
    print(
        f"{book_titles.get(book_id, f'Book {book_id}')}: "
        f"{average:.2f}/5 ({len(ratings)} reviews)"
    )
