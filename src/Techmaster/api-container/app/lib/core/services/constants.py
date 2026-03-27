from pydantic import BaseModel
from typing import TypeVar
from sqlalchemy.ext.automap import AutomapBase

modelType = TypeVar("modelType", bound=AutomapBase)
createSchemaType = TypeVar("createSchemaType", bound=BaseModel)
updateSchemaType = TypeVar("updateSchemaType", bound=BaseModel)