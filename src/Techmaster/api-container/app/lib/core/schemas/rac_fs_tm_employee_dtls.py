from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


def to_lower(string: str) -> str:
    return string.lower()


class racFsTmEmployeeDtlsBase(BaseModel):
    AREA_ID: Optional[int] = None
    EMPLOYEE_NAME: Optional[str] = None
    LOCATION_CODE: Optional[str] = None
    MANAGER_ID: Optional[int] = None
    JOB_ID: Optional[int] = None
    TEAM_TYPE_ID: Optional[int] = None
    WORK_SHIFT: Optional[str] = None
    ON_CALL: Optional[str] = None
    ON_SITE: Optional[str] = None
    DEDICATED: Optional[str] = None
    DEDICATED_TO: Optional[str] = None
    SERVICE_ADVANTAGE: Optional[str] = None
    SERVICE_START_DATE: Optional[datetime] = None
    SERVICE_END_DATE: Optional[datetime] = None
    FS_STATUS: Optional[str] = None
    RECORD_COMPLETE: Optional[str] = None
    ADMIN_NOTES: Optional[str] = None
    RECORD_COMPLETE: Optional[str] = None
    BUSINESS_ORG: Optional[str] = None
    ABSENCE_START_DATE: Optional[str] = None
    ABSENCE_END_DATE: Optional[str] = None
    ACTUAL_RETURN_TO_WORK: Optional[str] = None
    HR_STATUS: Optional[str] = None
    REVIEW_DATE: Optional[datetime] = None

    class Config:
        alias_generator = to_lower


class racFsTmEmployeeDtlsSchema(racFsTmEmployeeDtlsBase):
    LAST_UPDATE_BY: str = Field(alias="logged_in_user_id")
    LAST_UPDATE_DATE: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        alias_generator = to_lower
