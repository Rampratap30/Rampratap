import json
import os

from sqlalchemy import Column, ForeignKey, MetaData, Table, create_engine
from sqlalchemy.engine import URL
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from app.lib.aws.secret_manager import secretManager
import initialize


# Class declaration
class dbSession:
    # Get the database variable
    def __init__(self) -> None:
        try:
            
            self.sessionLocal = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=initialize.db_engine,
                expire_on_commit=False,
                class_=Session,
            )
        except Exception as e:
            raise e

    def __enter__(self) -> Session:
        """Create a new session"""
        self.session = self.sessionLocal()
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close the session and If an exception was raised in the `with` block, so roll back the transaction"""
        try:
            if exc_type is not None:
                self.session.rollback()
            else:
                self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise
        finally:
            self.session.close()
