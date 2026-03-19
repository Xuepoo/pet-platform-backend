from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ReportAuthor(BaseModel):
    """Author information for a report."""
    id: int
    full_name: Optional[str] = None
    avatar: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


class ReportBase(BaseModel):
    pet_name: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    report_type: Optional[str] = "lost"  # lost, found
    status: Optional[str] = "open"  # open, closed, resolved
    image_url: Optional[str] = None
    contact_info: Optional[str] = None


class ReportCreate(ReportBase):
    pass


class ReportUpdate(ReportBase):
    pass


class ReportInDBBase(ReportBase):
    id: int
    user_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)


class Report(ReportInDBBase):
    """Report response with author info."""
    author: Optional[ReportAuthor] = None


class ReportInDB(ReportInDBBase):
    pass
