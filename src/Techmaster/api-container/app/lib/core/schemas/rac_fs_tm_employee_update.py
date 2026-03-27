from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Extra, Field


def to_lower(string: str) -> str:
    return string.lower()


class racFsTmEmployeeUpdateBase(BaseModel):
    CHANGE_EFFECTIVE_DATE: Optional[datetime] = None
    EMPLOYEE_ID: Optional[int] = None
    EMPLOYEE_NAME: Optional[str] = None
    # JOB_CODE: Optional[str] = None
    JOB_TITLE: Optional[str] = None
    JOB_TYPE: Optional[str] = None
    # JOB_FAMILY: Optional[str] = None
    JOB_ADP: Optional[str] = None
    TEAM_TYPE: Optional[str] = None
    MANAGER_ID: Optional[int] = None
    MANAGER_FLAG: Optional[str] = None
    ADMIN_NOTES: Optional[str] = None
    SERVICE_START_DATE: Optional[datetime] = None
    SERVICE_END_DATE: Optional[datetime] = None
    WORK_SHIFT: Optional[str] = None
    ON_CALL: Optional[str] = None
    ON_SITE: Optional[str] = None
    SERVICE_ADVANTAGE: Optional[str] = None
    PRODUCTION_TYPE: Optional[str] = None
    RECORD_COMPLETE: Optional[str] = None
    DEDICATED: Optional[str] = None
    DEDICATED_TO: Optional[str] = None
    LOC_CODE: Optional[str] = None
    AREA: Optional[str] = None
    REGION: Optional[str] = None
    CHANGE_NOTE: Optional[str] = None
    CHANGE_TYPE: Optional[str] = None
    CHANGE_STATUS: Optional[str] = None
    FS_STATUS: Optional[str] = None
    REQUESTED_BY: Optional[str] = None
    APPROVAL_REQUIRED: Optional[str] = None
    APPROVED: Optional[str] = None
    APPROVED_BY: Optional[str] = None
    CSA_NOTIFICATION_REQUIRED: Optional[str] = None
    CSA_CHANGE_COMMENT: Optional[str] = None
    CSA_NOTIFICATION_COMPLETE: Optional[str] = None
    LAST_EDITED_DATE: Optional[datetime] = None
    LAST_EDITED_BY: Optional[str] = None
    PROCESSED_DATE: Optional[datetime] = None
    ATTRIBUTE1: Optional[str] = None
    ATTRIBUTE2: Optional[str] = None
    ATTRIBUTE3: Optional[str] = None
    ATTRIBUTE4: Optional[str] = None
    ATTRIBUTE5: Optional[str] = None
    ALTERNATE_EMAIL: Optional[str] = None
    PRODUCTION_PRINT: Optional[str] = None
    OFSC_STATUS: Optional[str] = None
    REVIEW_DATE: Optional[datetime] = None
    HR_STATUS: Optional[str] = None
    BUSINESS_ORG: Optional[str] = None
    ABSENCE_START_DATE: Optional[datetime] = None
    ABSENCE_END_DATE: Optional[datetime] = None
    ACTUAL_RETURN_TO_WORK: Optional[datetime] = None
    ALTERNATE_EMAIL_OLD: Optional[str] = None

    class Config:
        alias_generator = to_lower


class racFsTmEmployeeUpdateCreate(racFsTmEmployeeUpdateBase):
    CREATED_BY: str = Field(alias="logged_in_user_id")
    CREATION_DATE: datetime = Field(default_factory=datetime.utcnow)
    LAST_UPDATED_BY: str = Field(alias="logged_in_user_id")
    LAST_UPDATE_DATE: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        alias_generator = to_lower


class racFsTmEmployeeUpdateSchema(racFsTmEmployeeUpdateBase):
    LAST_UPDATED_BY: str = Field(alias="logged_in_user_id")
    LAST_UPDATE_DATE: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        alias_generator = to_lower


# class racFsTmEmployeeUpdateCommonBase(BaseModel):
#     CHANGE_EFFECTIVE_DATE: Optional[datetime] = None
#     EMPLOYEE_ID: Optional[int] = None
#     ADMIN_NOTES: Optional[str] = None
#     SERVICE_START_DATE: Optional[datetime] = None
#     SERVICE_END_DATE: Optional[datetime] = None
#     WORK_SHIFT: Optional[str] = None
#     ON_CALL: Optional[str] = None
#     ON_SITE: Optional[str] = None
#     SERVICE_ADVANTAGE: Optional[str] = None
#     PRODUCTION_TYPE: Optional[str] = None
#     RECORD_COMPLETE: Optional[str] = None
#     DEDICATED: Optional[str] = None
#     DEDICATED_TO: Optional[str] = None
#     CHANGE_STATUS: Optional[str] = None
#     TEAM_TYPE: Optional[str] = None
#     CHANGE_TYPE: Optional[str] = None
#     CHANGE_STATUS: Optional[str] = None
#     FS_STATUS: Optional[str] = None
#     REQUESTED_BY: Optional[str] = None
#     APPROVAL_REQUIRED: Optional[str] = None
#     APPROVED: Optional[str] = None
#     APPROVED_BY: Optional[str] = None
#     CSA_NOTIFICATION_REQUIRED: Optional[str] = None
#     CSA_CHANGE_COMMENT: Optional[str] = None
#     CSA_NOTIFICATION_COMPLETE: Optional[str] = None

#     class Config:
#         alias_generator = to_lower


class racFsTmEmployeeUpdateJob(racFsTmEmployeeUpdateBase):
    JOB_TITLE: Optional[str] = None
    JOB_FAMILY: Optional[str] = None
    JOB_ADP: Optional[str] = None
    ATTRIBUTE1: Optional[str] = None
    LAST_UPDATED_BY: str = Field(alias="logged_in_user_id")
    LAST_UPDATE_DATE: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        alias_generator = to_lower


class racFsTmEmployeeUpdateHierarchy(racFsTmEmployeeUpdateBase):
    LOC_CODE: Optional[str] = None
    AREA: Optional[str] = None
    REGION: Optional[str] = None
    ATTRIBUTE2: Optional[str] = None
    LAST_UPDATED_BY: str = Field(alias="logged_in_user_id")
    LAST_UPDATE_DATE: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        alias_generator = to_lower


class racFsTmEmployeeUpdateManager(racFsTmEmployeeUpdateBase):
    MANAGER_ID: Optional[int] = None
    MANAGER_FLAG: Optional[str] = None
    ATTRIBUTE3: Optional[str] = None
    LAST_UPDATED_BY: str = Field(alias="logged_in_user_id")
    LAST_UPDATE_DATE: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        alias_generator = to_lower
