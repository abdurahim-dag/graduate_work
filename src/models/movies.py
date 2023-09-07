"""Модели источника о фильмах."""
from typing import Optional
from uuid import UUID

from pendulum import DateTime
from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import field_validator


class UUIDMixin(BaseModel):
    id: UUID


class DateUUIDMixin(UUIDMixin):
    created: DateTime
    modified: DateTime

    model_config = ConfigDict(arbitrary_types_allowed=True)


class Genre(DateUUIDMixin):
    __table_name__ = 'genre'
    name: str
    description: Optional[str]


class Person(DateUUIDMixin):
    __table_name__ = 'person'
    full_name: str


class Movie(DateUUIDMixin):
    __table_name__ = 'film_work'

    rating: Optional[float]
    creation_date: Optional[DateTime]
    title: Optional[str]
    type: Optional[str]
    description: Optional[str]

    @field_validator('rating')
    @classmethod
    def fix_raiting(cls, v):
        if v is not None:
            if v < 0:
                v = 0
            elif v > 100:
                v = 100
        return v

class GenreFilmWork(UUIDMixin):
    __table_name__ = 'genre_film_work'
    model_config = ConfigDict(arbitrary_types_allowed=True)
    film_work_id: UUID
    genre_id: UUID
    created: DateTime


class PersonFilmWork(UUIDMixin):
    __table_name__ = 'person_film_work'
    model_config = ConfigDict(arbitrary_types_allowed=True)
    film_work_id: UUID
    person_id: UUID
    role: str
    created: DateTime