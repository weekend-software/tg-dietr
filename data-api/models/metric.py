from datetime import datetime
from typing import Optional
from pydantic import BaseModel, validator


class Metric(BaseModel):
    name: str
    value: float
    measured_at: Optional[datetime] = datetime.now()

    @validator("name")
    def name_must_not_be_empty(cls, v):
        if v.strip() == "":
            raise ValueError("Must not be empty")
        return v

    @validator("value")
    def value_must_be_positive(cls, v):
        if v < 0:
            raise ValueError("Must not be negative")
        return v
