from datetime import datetime
from typing import Optional
from pydantic import BaseModel, validator


class User(BaseModel):
    id: int
    created_at: Optional[datetime] = datetime.now()
    activated_at: Optional[datetime] = datetime.now()
    deactivated_at: Optional[datetime] = datetime.fromtimestamp(0)
    is_active: Optional[bool] = None

    @validator("is_active", always=True)
    def is_active_now(cls, v, values):
        return values.get("activated_at").timestamp() > values.get("deactivated_at").timestamp()

    @validator("id")
    def id_must_not_be_null(cls, v):
        if v == 0:
            raise ValueError("Must not be equal to 0")
        return v
