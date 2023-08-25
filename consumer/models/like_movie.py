from uuid import UUID

from .base import Score


class FilmScore(Score):
    film_id: UUID
    user_id: UUID
