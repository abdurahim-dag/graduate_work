from pendulum import Date
from pydantic import BaseModel


class EtlState(BaseModel):
    date_from: Date | None
    date_to: Date | None
    step: int | None
