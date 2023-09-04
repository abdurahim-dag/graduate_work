from pathlib import Path
from uuid import UUID
from typing import Any

from pendulum import Date
from pydantic import (
    BaseModel,
    Field,
    field_validator,
    BaseSettings,
)
from typing import Any


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

    @field_validator('imdb_rating')
    @classmethod
    def fix_raiting(cls, v):
        if v < 0:
            v = 0
        elif v > 100:
            v = 100
        return v
