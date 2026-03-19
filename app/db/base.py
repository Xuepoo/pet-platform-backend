"""Database model imports for Alembic migrations.

This module imports all SQLAlchemy models so that the Base metadata
contains all table definitions when used by Alembic for migrations.
"""

from app.db.base_class import Base  # noqa
from app.models.application import Application  # noqa
from app.models.pet import Pet  # noqa
from app.models.report import Report  # noqa
from app.models.user import User  # noqa
