"""Application model for pet adoption requests.

This module defines the Application SQLAlchemy model for tracking
adoption application submissions and their status.
"""

from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Application(Base):
    """Adoption application model.
    
    Tracks user requests to adopt specific pets with approval workflow.
    
    Attributes:
        id: Primary key.
        pet_id: Foreign key to the pet being applied for.
        user_id: Foreign key to the applicant user.
        message: Optional message from the applicant.
        status: Application status (pending, approved, rejected).
        created_at: Timestamp of application submission.
        pet: Relationship to the pet.
        user: Relationship to the applicant user.
    """
    
    id = Column(Integer, primary_key=True, index=True)
    pet_id = Column(Integer, ForeignKey("pet.id"))
    user_id = Column(Integer, ForeignKey("user.id"))
    message = Column(String, nullable=True)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)

    pet = relationship("Pet", back_populates="applications")
    user = relationship("User", back_populates="applications")
