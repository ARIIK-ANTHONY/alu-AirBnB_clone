#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import models
from uuid import uuid4
from datetime import datetime, timezone
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, String

Base = declarative_base()


class BaseModel:
    """Defines the BaseModel class.

    Attributes:
        id (sqlalchemy String): The BaseModel id.
        created_at (sqlalchemy DateTime): The datetime at creation.
        updated_at (sqlalchemy DateTime): The datetime of last update.
    """

    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    def __init__(self, *args, **kwargs):
        """Initialize a new BaseModel."""
        self.id = str(uuid4())
        self.created_at = self.updated_at = datetime.now(timezone.utc)

        kwargs.pop("__class__", None)
        if kwargs:
            for key, value in kwargs.items():
                if key in ("created_at", "updated_at") and isinstance(value, str):
                    try:
                        value = datetime.fromisoformat(value)
                    except ValueError:
                        # Fallback for datetime strings without timezone
                        value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f").replace(tzinfo=timezone.utc)
                setattr(self, key, value)

        self.updated_at = datetime.now(timezone.utc)

    def save(self):
        """Update updated_at with the current datetime."""
        self.updated_at = datetime.now(timezone.utc)
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Return a dictionary representation of the BaseModel instance."""
        my_dict = self.__dict__.copy()
        my_dict["__class__"] = str(type(self).__name__)
        my_dict["created_at"] = self.created_at.isoformat()
        my_dict["updated_at"] = self.updated_at.isoformat()
        my_dict.pop("_sa_instance_state", None)
        return my_dict

    def delete(self):
        """Delete the current instance from storage."""
        models.storage.delete(self)

    def __str__(self):
        """Return the print/str representation of the BaseModel instance."""
        d = self.__dict__.copy()
        d.pop("_sa_instance_state", None)
        return "[{}] ({}) {}".format(type(self).__name__, self.id, d)
