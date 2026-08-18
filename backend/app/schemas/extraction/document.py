from pydantic import BaseModel


class DocumentV1(BaseModel):
    title: str

    author: str = ""

    genre: str = ""

    language: str = ""

    pages: int = 0

    summary: str = ""