# Bookshop Reviews — SAP CAP Project

A simple bookshop application built using **SAP Cloud Application Programming Model (CAP)**, Node.js, CDS, SQLite, and Python. This project extends the original Bookshop application with a Reviews entity, server-side rating validation, and a Python script that calculates average book ratings.

## Features

- **Book and Author Management:** Uses the existing CAP data model for books and authors.
- **Book Reviews:** Stores ratings and comments associated with individual books.
- **Rating Validation:** Rejects review creation requests when the rating is not an integer between 1 and 5.
- **OData V4 API:** Exposes Books, Authors, and Reviews through the CatalogService.
- **Python Integration:** Posts three reviews through HTTP requests and calculates the average rating for each book.
- **SQLite Database:** Uses the CAP SQLite adapter with an in-memory database during local development.

## Technology Stack

- SAP Cloud Application Programming Model (CAP)
- CDS (Core Data Services)
- Node.js
- JavaScript
- SQLite
- OData V4
- Python 3
- Python `requests` library

## Project Structure

```text
bookshop/
├── db/
│   ├── schema.cds
│   └── data/
│       ├── my.bookshop-Books.csv
│       └── my.bookshop-Authors.csv
├── srv/
│   ├── cat-service.cds
│   └── cat-service.js
├── post_reviews.py
├── package.json
├── package-lock.json
└── README.md
```

## Data Model

### Books

The existing Books entity contains the book's ID, title, stock, price, and association to its author.

### Authors

The Authors entity stores author information and has an association to their books.

### Reviews

The new Reviews entity contains:

| Field | Description |
|---|---|
| `ID` | Unique review identifier |
| `rating` | Integer rating from 1 to 5 |
| `comment` | Text describing the review |
| `book` | Association linking the review to a book |

The Reviews entity uses CAP's managed aspect for standard creation and modification metadata.

## Rating Validation

The `srv/cat-service.js` file implements a `before('CREATE', Reviews)` handler.

Before a review is created, the handler checks whether its rating is an integer within the permitted range of 1–5.

- Ratings from 1 to 5 are accepted.
- Ratings below 1 or above 5 are rejected.
- Non-integer ratings are rejected.
- Invalid requests receive an HTTP 400 error with a descriptive validation message.

This ensures that invalid ratings are rejected by the backend instead of relying only on client-side validation.

## API Endpoints

The CatalogService is available at:

`http://localhost:4004/odata/v4/catalog`

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/Books` | Retrieve books |
| GET | `/Authors` | Retrieve authors |
| GET | `/Reviews` | Retrieve reviews |
| POST | `/Reviews` | Create a review |

For example, a review can be submitted to:

`POST http://localhost:4004/odata/v4/catalog/Reviews`

Example request body:

```json
{
  "rating": 5,
  "comment": "Excellent book!",
  "book_ID": 1
}
```

Use an existing book ID when submitting a review.

## Prerequisites

Install the following before running the project:

- Node.js — preferably Node.js 24 for compatibility with the current SQLite dependency configuration.
- npm, which is included with Node.js.
- Python 3.
- Git, if you want to clone the repository.

## Installation and Setup

### 1. Install Node.js dependencies

From the project directory, run:

```powershell
npm install
```

### 2. Install the Python dependency

```powershell
python -m pip install requests
```

Using a Python virtual environment is recommended to isolate Python dependencies.

### 3. Start the CAP application

```powershell
npx cds watch
```

The application should start at:

`http://localhost:4004`

The CatalogService endpoint is:

`http://localhost:4004/odata/v4/catalog`

CAP deploys the model and available CSV sample data when the development server starts.

## Running the Python Review Script

Keep the CAP server running in one terminal. Open a second terminal in the project directory and execute:

```powershell
python post_reviews.py
```

The script:

1. Retrieves available books from the CAP OData service.
2. Creates three reviews using HTTP POST requests.
3. Retrieves the reviews from the service.
4. Groups ratings by book.
5. Calculates and prints the average rating for each book.

### Example Output

```text
Posted review with rating 5
Posted review with rating 4
Posted review with rating 3

Average rating per book:
Wuthering Heights: 4.50/5 (2 reviews)
The Raven -- 11% off!: 3.00/5 (1 review)
```

The displayed book names and average ratings may vary depending on the available books and reviews.

## Existing Book Discount Logic

The original service implementation adds the label `-- 11% off!` to book titles when their stock exceeds 100. This behavior is retained in the updated service.

## Database Notes

The local development setup uses an in-memory SQLite database. Data created during a session is lost when the CAP server restarts.

The Python script adds reviews to the current database, so running it repeatedly without restarting the server can increase the number of reviews included in the averages.

## Assignment Requirements Completed

1. Added a Reviews entity with ratings and comments linked to Books.
2. Implemented backend validation to reject ratings outside the range 1–5.
3. Developed a Python script that posts three reviews and prints the average rating per book.

## Future Improvements

- Persist review data in a file-backed or production database.
- Add automated tests for valid and invalid ratings.
- Expose aggregated ratings through a dedicated service endpoint.
- Improve review management and error handling.

## License

This project uses the license configuration specified in `package.json`. Check the repository's licensing requirements before redistributing the project.
