from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field


def to_lower(string: str) -> str:
    return string.lower()


class racFsTmLogs(BaseModel):
    EMAIL_ID: str
    FILE_NAME: Optional[str] = None
    LAMBDA_STATUS: Optional[str] = None
    PROCEDURE_NAME: Optional[str] = None
    MSG: Optional[str] = None
    TYPE: Optional[str] = None
    ATTRIBUTE1: Optional[str] = None
    ATTRIBUTE2: Optional[str] = None
    ATTRIBUTE3: Optional[str] = None
    ATTRIBUTE4: Optional[str] = None
    ATTRIBUTE5: Optional[str] = None

    class Config:
        alias_generator = to_lower


class racFsTmLogsCreate(racFsTmLogs):
    CREATED_BY: str = Field(alias="logged_in_user_id")
    CREATION_DATE: datetime = Field(default_factory=datetime.utcnow)
    LAST_UPDATED_BY: str = Field(alias="logged_in_user_id")
    LAST_UPDATE_DATE: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        alias_generator = to_lower


class racFsTmLogsUpdate(racFsTmLogs):
    LAST_UPDATED_BY: str = Field(alias="logged_in_user_id")
    LAST_UPDATE_DATE: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        alias_generator = to_lower
