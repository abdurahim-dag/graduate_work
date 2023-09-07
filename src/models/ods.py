"""Модели центрального слоя, для выгрузок"""
import datetime
import uuid
from typing import List

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy import UUID
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class CommonMixin:
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)



person_film_work = Table(
    "person_film_work",
    Base.metadata,
    Column("id", UUID, primary_key=True),
    Column("role", String()),
    Column("created", DateTime),
    Column("film_work_id", UUID, ForeignKey("film_work.id")),
    Column("person_id", UUID, ForeignKey("person.id")),
)

genre_film_work = Table(
    "genre_film_work",
    Base.metadata,
    Column("id", UUID, primary_key=True),
    Column("created", DateTime),
    Column("film_work_id", UUID, ForeignKey("film_work.id")),
    Column("genre_id", UUID, ForeignKey("genre.id")),
)

class PersonFilmWork(CommonMixin, Base):
    __tablename__ = "person_film_work"
    __table_args__ = {'extend_existing': True}

    role: Mapped[str]
    created: Mapped[datetime.datetime]
    film_work_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("film_work.id"))
    person_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("person.id"))


class GenreFilmWork(CommonMixin, Base):
    __tablename__ = "genre_film_work"
    __table_args__ = {'extend_existing': True}

    created: Mapped[datetime.datetime]
    film_work_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("film_work.id"))
    genre_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("genre.id"))


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

class DLQ(Base):
    __tablename__ = "dlq"

    id: Mapped[int] = mapped_column(primary_key=True)
    obj: Mapped[str]
    description: Mapped[str]
