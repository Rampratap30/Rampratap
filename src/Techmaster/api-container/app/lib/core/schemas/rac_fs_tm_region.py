from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field


def to_lower(string: str) -> str:
    return string.lower()


class racFsTmRegionBase(BaseModel):
    REGION_NAME: str
    REGION_SHORT_NAME: Optional[str] = None
    REGION_DIR_EMP_ID: Optional[int] = None
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


class racFsTmRegionCreate(racFsTmRegionBase):
    EFFECTIVE_START_DATE: datetime
    CREATED_BY: str = Field(alias="logged_in_user_id")
    CREATION_DATE: datetime = Field(default_factory=datetime.utcnow)
    LAST_UPDATED_BY: str = Field(alias="logged_in_user_id")
    LAST_UPDATE_DATE: datetime = Field(default_factory=datetime.utcnow)
    STATUS: str

    class Config:
        alias_generator = to_lower


class racFsTmRegionUpdate(racFsTmRegionBase):
    LAST_UPDATED_BY: str = Field(alias="logged_in_user_id")
    LAST_UPDATE_DATE: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        alias_generator = to_lower
