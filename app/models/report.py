"""Report model for lost and found pets.

This module defines the Report SQLAlchemy model for tracking
lost and found pet reports.
"""

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Report(Base):
    """Lost and found pet report model.
    
    Allows users to report lost pets or found pets with location
    and contact information.
    
    Attributes:
        id: Primary key.
        pet_name: Name of the lost/found pet.
        description: Detailed description of the pet.
        location: Where the pet was lost or found.
        report_type: Type of report (lost, found).
        status: Report status (open, closed, resolved).
        image_url: Optional image URL of the pet.
        contact_info: Contact information for the reporter.
        user_id: Foreign key to the reporting user.
        user: Relationship to the user.
    """
    
    id = Column(Integer, primary_key=True, index=True)
    pet_name = Column(String, index=True)
    description = Column(String)
    location = Column(String)
    report_type = Column(String, default="lost")
    status = Column(String, default="open")
    image_url = Column(String, nullable=True)
    contact_info = Column(String)
    user_id = Column(Integer, ForeignKey("user.id"))

    user = relationship("User", back_populates="reports")
