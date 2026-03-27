from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, List, Optional, Type, Union

from sqlalchemy import Row, desc, func, select
from sqlalchemy.orm.session import Session

from app.lib.core.services.constants import (
    createSchemaType,
    modelType,
    updateSchemaType,
)


class baseService(Generic[createSchemaType, updateSchemaType]):
    """Implemented base CRUD operations using SQLAlchemy"""

    def __init__(self, model: Type[modelType], session: Session):
        self.model = model
        self.session = session

    def get_count(self) -> int:
        """Get table record count"""
        result = self.session.execute(
            select(func.count()).select_from(select(self.model).subquery())
        )
        return result.scalar_one()

    def get_all(self) -> List[modelType]:
        """Get an instance all records"""
        return self.session.query(self.model).all()

    def get_pk_id(self, primary_id: int) -> Optional[modelType]:
        return self.session.query(self.model).get(primary_id)

    def create(self, instance: createSchemaType) -> modelType:
        new_row = self.model(**instance.dict())
        self.session.add(new_row)
        self.session.flush()
        return new_row

    def update(
        self, current_instance: modelType, update_instance: updateSchemaType
    ) -> modelType:
        update_row = dict(update_instance)
        for key, value in update_row.items():
            setattr(current_instance, key, value)

        # Update value
        self.session.add(current_instance)
        self.session.flush()

        # Update existing instance value
        self.session.refresh(current_instance)

        return current_instance
