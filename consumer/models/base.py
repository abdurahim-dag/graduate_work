import pendulum
from pydantic import BaseModel, validator


class Base(BaseModel):
    timestamp: pendulum.DateTime

    @validator('timestamp', pre=True)
    def ensure_datetime(cls, v):
        return pendulum.parse(v)


class Score(Base):
    score: int

    @validator('score')
    def ensure_score(cls, v):
        if 0 > v or v > 10:
            raise ValueError('score must be >=0 and <=10')
        return v
