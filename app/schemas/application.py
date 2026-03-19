from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict
from .pet import Pet


class ApplicationBase(BaseModel):
    status: Optional[str] = "pending"  # pending, approved, rejected
    message: Optional[str] = None


class ApplicationCreate(ApplicationBase):
    pet_id: int
    message: str


class ApplicationUpdate(ApplicationBase):
    pass


class ApplicationInDBBase(ApplicationBase):
    id: int
    pet_id: int
    user_id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class Application(ApplicationInDBBase):
    pet: Optional[Pet] = None


class ApplicationInDB(ApplicationInDBBase):
    pass
