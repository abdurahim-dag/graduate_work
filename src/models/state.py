from pendulum import DateTime
from pydantic import BaseModel, ConfigDict


class EtlState(BaseModel):
    date_from: DateTime = DateTime(2020,1,1)
    date_to: DateTime | None = None
    offset: int = 0

    model_config = ConfigDict(arbitrary_types_allowed=True)
