from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


def to_lower(string: str) -> str:
    return string.lower()


class racFsTmNotificationBase(BaseModel):
    NOTIFICATION_NAME: str
    EMAIL_ID: Optional[str] = None
    NOTIFICATION_SUBJECT: Optional[str] = None
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


class racFsTmNotificationCreate(racFsTmNotificationBase):
    EFFECTIVE_START_DATE: datetime
    CREATED_BY: str = Field(alias="logged_in_user_id")
    CREATION_DATE: datetime = Field(default_factory=datetime.utcnow)
    LAST_UPDATED_BY: str = Field(alias="logged_in_user_id")
    LAST_UPDATE_DATE: datetime = Field(default_factory=datetime.utcnow)
    STATUS: str

    class Config:
        alias_generator = to_lower


class racFsTmNotificationUpdate(racFsTmNotificationBase):
    LAST_UPDATED_BY: str = Field(alias="logged_in_user_id")
    LAST_UPDATE_DATE: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        alias_generator = to_lower
