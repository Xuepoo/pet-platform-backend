# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.application import Application  # noqa
from app.models.pet import Pet  # noqa
from app.models.report import Report  # noqa
from app.models.user import User  # noqa
