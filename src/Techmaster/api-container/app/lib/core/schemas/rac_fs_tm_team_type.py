from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field


def to_lower(string: str) -> str:
    return string.lower()


class racFsTmTeamTypeBase(BaseModel):
    TEAM_TYPE_NAME: str
    STATUS: Optional[str] = None
    EFFECTIVE_START_DATE: Optional[datetime] = None
    EFFECTIVE_END_DATE: Optional[datetime] = None

    class Config:
        alias_generator = to_lower


class racFsTmTeamTypeCreate(racFsTmTeamTypeBase):
    EFFECTIVE_START_DATE: datetime
    CREATED_BY: str = Field(alias="logged_in_user_id")
    CREATION_DATE: datetime = Field(default_factory=datetime.utcnow)
    LAST_UPDATED_BY: str = Field(alias="logged_in_user_id")
    LAST_UPDATE_DATE: datetime = Field(default_factory=datetime.utcnow)
    STATUS: str

    class Config:
        alias_generator = to_lower


class racFsTmTeamTypeUpdate(racFsTmTeamTypeBase):
    LAST_UPDATED_BY: str = Field(alias="logged_in_user_id")
    LAST_UPDATE_DATE: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        alias_generator = to_lower
