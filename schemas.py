from pydantic import BaseModel, ConfigDict


class BookModel(BaseModel):
    id: int
    title: str
    author: str
    description: str
    price: float
    is_available: bool

    model_config = ConfigDict(from_attributes=True)


class CreateBookModel(BaseModel):
    title: str
    author: str
    description: str
    price: float
    is_available: bool
