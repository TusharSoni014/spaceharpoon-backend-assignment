from fastapi import FastAPI
from crud import Crud
from models import Books
from schemas import BookModel, CreateBookModel
from db import engine
from sqlalchemy.ext.asyncio import async_sessionmaker

app = FastAPI(docs_url="/docs", title="BookStore API")

session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)

db = Crud(session)


@app.get("/all-books", response_model=list[BookModel])
async def get_all_books(is_available: bool | None = None):
    books = await db.get_all_books(is_available)
    return books


@app.get("/book/{book_id}")
async def get_a_book(book_id: int):
    book = await db.get_a_book(book_id)
    return book


@app.post("/create-book")
async def create_book(book: CreateBookModel):
    new_book = await db.create_book(book)
    return new_book


@app.put("/update-book")
async def update_book(book_id: int, book: CreateBookModel):
    updated_book = await db.update_book(book_id, Books(**book.model_dump()))
    return updated_book


@app.delete("/delete-book/{book_id}")
async def delete_book(book_id: int):
    book = await db.delete_book(book_id)
    return book
