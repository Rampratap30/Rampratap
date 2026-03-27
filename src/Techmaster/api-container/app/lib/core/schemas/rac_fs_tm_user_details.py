from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field


def to_lower(string: str) -> str:
    return string.lower()

class racFsTmUserDetailsBase(BaseModel):
    EMPLOYEE_ID: Optional[int] = None
    EMPLOYEE_NAME: Optional[str] = None
    EMAIL: Optional[str] = None
    ROLE: Optional[str] = None
    LAST_LOGIN: Optional[datetime] = None

    class Config:
        alias_generator = to_lower
