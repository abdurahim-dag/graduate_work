import datetime

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped


class Base(DeclarativeBase):
    obj: Mapped[str]


class TimeStampedMixin:
    modified: Mapped[datetime.datetime]

class Movie(TimeStampedMixin, Base):
    __tablename__ = "v_movies"


class Role(TimeStampedMixin, Base):
    __tablename__ = "v_roles"


class Genre(TimeStampedMixin, Base):
    __tablename__ = "v_genres"
