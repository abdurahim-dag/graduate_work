from pendulum import Date
from pydantic import BaseModel


class EtlState(BaseModel):
    date_from: Date = Date(2023,1,1)
    date_to: Date | None
    offset: int = 0
