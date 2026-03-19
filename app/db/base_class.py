"""SQLAlchemy declarative base class.

This module defines the base class for all SQLAlchemy ORM models
with automatic table name generation.
"""

from typing import Any

from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    """Base class for all SQLAlchemy ORM models.
    
    Provides automatic table name generation based on the class name
    and a common id attribute declaration.
    
    Attributes:
        id: Primary key column (defined in subclasses).
        __name__: Class name used for table name generation.
    """
    
    id: Any
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        """Generate table name from class name in lowercase.
        
        Returns:
            The lowercase version of the class name.
        """
        return cls.__name__.lower()
