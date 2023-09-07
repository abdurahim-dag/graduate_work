"""Модели, для индексов ES."""
from uuid import UUID

from pydantic import BaseModel, Field


class UUIDMixin(BaseModel):
    id: UUID


class GenreName(UUIDMixin):
    name: str


class Genre(GenreName):
    description: str


class PersonName(UUIDMixin):
    name: str


class Person(UUIDMixin):
    full_name: str
    role: str
    film_ids: list[str] | None


class Movie(UUIDMixin):
    imdb_rating: float
    genre: list[GenreName]

    title: str
    description: str | None

    directors: list[PersonName]
    actors: list[PersonName]
    writers: list[PersonName]

    actors_names: list[str] | None
    writers_names: list[str] | None


class ESIndex(BaseModel):
    id: UUID = Field(None, alias="_id")
    index: str = Field(None, alias="_index")


class ESIndexLine(BaseModel):
    index: ESIndex
