from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from models import Books
from schemas import CreateBookModel


class Crud:
    def __init__(self, db_session: async_sessionmaker[AsyncSession]):
        self.db_session = db_session

    async def create_book(self, book: CreateBookModel):
        async with self.db_session() as session:
            db_book = Books(
                title=book.title,
                author=book.author,
                description=book.description,
                price=book.price,
                is_available=book.is_available,
            )
            session.add(db_book)
            await session.commit()
            return db_book

    async def get_all_books(self, is_available: bool | None = None):
        async with self.db_session() as session:
            statement = select(Books)
            if is_available is not None:
                statement = statement.where(Books.is_available == is_available)
            books = await session.execute(statement)
            return books.scalars()

    async def get_a_book(self, book_id: int):
        async with self.db_session() as session:
            statement = select(Books).where(Books.id == book_id)
            book = await session.execute(statement)
            if not book:
                raise HTTPException(status_code=404, detail="Book Not found!")
            return book.scalars().one()

    async def update_book(self, book_id: int, updated_book: Books):
        async with self.db_session() as session:
            statement = select(Books).where(Books.id == book_id)
            book = (await session.execute(statement)).scalars().one()
            if not book:
                raise HTTPException(status_code=404, detail="Book Not found!")
            if updated_book.author is not None:
                book.author = updated_book.author
            if updated_book.description is not None:
                book.description = updated_book.description
            if updated_book.is_available is not None:
                book.is_available = updated_book.is_available
            if updated_book.price is not None:
                book.price = updated_book.price
            if updated_book.title is not None:
                book.title = updated_book.title
            await session.commit()
            return book

    async def delete_book(self, book_id: int):
        async with self.db_session() as session:
            statement = select(Books).where(Books.id == book_id)
            book = (await session.execute(statement)).scalars().one()
            if not book:
                raise HTTPException(status_code=404, detail="Book Not found!")
            await session.delete(book)
            return {"message": "book deleted success!"}
