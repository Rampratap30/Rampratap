from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field


def to_lower(string: str) -> str:
    return string.lower()


class racFsTmAreaBase(BaseModel):
    REGION_ID: Optional[int] = None
    AREA_SHORT_NAME: Optional[str] = None
    AREA_DIR_EMP_ID: Optional[int] = None
    AREA_FOM_EMP_ID: Optional[int] = None
    ATTRIBUTE1: Optional[str] = None
    ATTRIBUTE2: Optional[str] = None
    ATTRIBUTE3: Optional[str] = None
    ATTRIBUTE4: Optional[str] = None
    ATTRIBUTE5: Optional[str] = None
    EFFECTIVE_START_DATE: Optional[datetime] = None
    EFFECTIVE_END_DATE: Optional[datetime] = None
    STATUS: Optional[str] = None

    class Config:
        alias_generator = to_lower


class racFsTmAreaCreate(racFsTmAreaBase):
    EFFECTIVE_START_DATE: datetime
    CREATED_BY: str = Field(alias="logged_in_user_id")
    CREATION_DATE: datetime = Field(default_factory=datetime.utcnow)
    LAST_UPDATED_BY: str = Field(alias="logged_in_user_id")
    LAST_UPDATE_DATE: datetime = Field(default_factory=datetime.utcnow)
    STATUS: str

    class Config:
        alias_generator = to_lower


class racFsTmAreaUpdate(racFsTmAreaBase):
    LAST_UPDATED_BY: str = Field(alias="logged_in_user_id")
    LAST_UPDATE_DATE: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        alias_generator = to_lower
