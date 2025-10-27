from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from starlette import status

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class Bookrequest(BaseModel):
    id: Optional[int] = Field(
        description='ID is not needed on create.', default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=6)
    published_date: int = Field(gt=1999, lt=2031)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new book",
                "author": "codingwithroby",
                "description": "A new description of a book",
                "rating": 5,
                "published_date": 2012
            }
        }
    }


BOOKS: List[Book] = [
    Book(1, 'Computer Science Pro', 'codingwithroby',
         'A very nice book!', 5, 2010),
    Book(2, 'Be fast with FastAPI', 'codingwithroby', 'A great book!', 5, 2012),
    Book(3, 'Master Endpoints', 'codingwithroby', 'An awesome book!', 5, 2012),
    Book(4, 'HP1', 'Author 1', 'Book description 1!', 3, 2015),
    Book(5, 'HP2', 'Author 2', 'Book description 2!', 2, 2016),
    Book(6, 'HP3', 'Author 3', 'Book description 3!', 1, 2017),
]


@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS


@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book_by_id(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail='Item not found.')


@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_books_by_rating(book_rating: int = Query(ge=0, le=5)):
    return [book for book in BOOKS if book.rating == book_rating]


@app.get("/books/published-date/", status_code=status.HTTP_200_OK)
async def read_books_by_publish_date(book_published_date: int = Query(gt=1999, lt=2031)):
    return [book for book in BOOKS if book.published_date == book_published_date]


@app.post("/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: Bookrequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))
    return new_book


def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1

    return book


@app.put("/book/update-book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: Bookrequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_changed = True
    if not book_changed:
        raise HTTPException(status_code=404, detail='Item not found.')


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    book_deleted = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_deleted = True
            break
    if not book_deleted:
        raise HTTPException(status_code=404, detail='Item not found.')
