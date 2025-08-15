from pydantic import BaseModel

class Book(BaseModel):
    book_id: int
    title: str
    author: str
    genre: str

class Rating(BaseModel):
    user_id: int
    book_id: int
    rating: int
