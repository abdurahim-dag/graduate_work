from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy import Table, Column, UUID
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
import datetime
import uuid

class Base(DeclarativeBase):
    pass


class CommonMixin:
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)



person_film_work = Table(
    "person_film_work",
    Base.metadata,
    Column("id", UUID, primary_key=True),
    Column("role", String()),
    Column("film_work", UUID, ForeignKey("film_work.id")),
    Column("person", UUID, ForeignKey("person.id")),
)

genre_film_work = Table(
    "genre_film_work",
    Base.metadata,
    Column("id", UUID, primary_key=True),
    Column("film_work", UUID, ForeignKey("film_work.id")),
    Column("genre", UUID, ForeignKey("genre.id")),
)


class TimeStampedMixin:
    created: Mapped[datetime.datetime]
    modified: Mapped[datetime.datetime]

class Genre(CommonMixin, TimeStampedMixin, Base):
    __tablename__ = "genre"

    name: Mapped[str]
    description: Mapped[str]

class Person(CommonMixin, TimeStampedMixin, Base):
    __tablename__ = "person"

    full_name: Mapped[str]


class FilmWork(CommonMixin, TimeStampedMixin, Base):
    __tablename__ = "film_work"

    title: Mapped[str]
    description: Mapped[str]
    creation_date: Mapped[datetime.datetime]
    rating: Mapped[float]
    type: Mapped[str]
    genres: Mapped[List[Genre]] = relationship(secondary=genre_film_work)
    person: Mapped[List[Person]] = relationship(secondary=person_film_work)
