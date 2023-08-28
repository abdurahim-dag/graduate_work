from .base import QueryBuilderBase
from models import EventSubscription

class SQLQueryBuilder(QueryBuilderBase):

    def __init__(self, settings: EventSubscription):
        self._settings = settings

    def _build(self):

