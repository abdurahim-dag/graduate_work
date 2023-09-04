from pendulum import DateTime
from uuid import UUID
from typing import Annotated, get_origin, Optional
from pendulum import Date
from pydantic import (
    BaseModel,
    ConfigDict,
    field_validator,
    FieldValidationInfo
 )



class UUIDMixin(BaseModel):
    id: UUID

class DateUUIDMixin(UUIDMixin):
    created: DateTime
    modified: DateTime

    model_config = ConfigDict(arbitrary_types_allowed=True)

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


class Movie(DateUUIDMixin):
    rating: Optional[float]
    creation_date: Optional[DateTime]

    title: Optional[str]
    type: Optional[str]
    description: Optional[str]

    __table_name__ = 'film_work'


    @field_validator('rating')
    @classmethod
    def fix_raiting(cls, v):
        if v is not None:
            if v < 0:
                v = 0
            elif v > 100:
                v = 100
        return v
