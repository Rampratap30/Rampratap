from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field


def to_lower(string: str) -> str:
    return string.lower()


class racFsTmJobCodeBase(BaseModel):
    #JOB_CODE: Optional[int] = None
    JOB_TITLE: Optional[str] = None
    #JOB_FAMILY: Optional[str] = None
    JOB_TYPE: Optional[str] = None
    #BUS_TYPE: Optional[str] = None
    JOB_ADP_CODE: Optional[str] = None
    MANAGER_FLAG: Optional[str] = None
    AUTO_ADD: Optional[str] = None
    APPROVAL_REQUIRED: Optional[str] = None
    ATTRIBUTE1: Optional[str] = None
    ATTRIBUTE2: Optional[str] = None
    ATTRIBUTE3: Optional[str] = None
    ATTRIBUTE4: Optional[str] = None
    ATTRIBUTE5: Optional[str] = None
    STATUS: Optional[str] = None
    EFFECTIVE_START_DATE: Optional[datetime] = None
    EFFECTIVE_END_DATE: Optional[datetime] = None

    class Config:
        alias_generator = to_lower


class racFsTmJobCodeCreate(racFsTmJobCodeBase):
    EFFECTIVE_START_DATE: datetime
    CREATED_BY: str = Field(alias="logged_in_user_id")
    CREATION_DATE: datetime = Field(default_factory=datetime.utcnow)
    LAST_UPDATED_BY: str = Field(alias="logged_in_user_id")
    LAST_UPDATE_DATE: datetime = Field(default_factory=datetime.utcnow)
    STATUS: str

    class Config:
        alias_generator = to_lower


class racFsTmJobCodeUpdate(racFsTmJobCodeBase):
    LAST_UPDATED_BY: str = Field(alias="logged_in_user_id")
    LAST_UPDATE_DATE: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        alias_generator = to_lower
