from typing import Optional

from pydantic import BaseModel, ConfigDict


class ReportBase(BaseModel):
    pet_name: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    report_type: Optional[str] = "lost" # lost, found
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
    model_config = ConfigDict(from_attributes=True)


class Report(ReportInDBBase):
    pass


class ReportInDB(ReportInDBBase):
    pass
