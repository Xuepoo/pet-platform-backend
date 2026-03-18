from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Application(Base):
    id = Column(Integer, primary_key=True, index=True)
    pet_id = Column(Integer, ForeignKey("pet.id"))
    user_id = Column(Integer, ForeignKey("user.id"))
    message = Column(String, nullable=True)
    status = Column(String, default="pending")  # pending, approved, rejected
    created_at = Column(DateTime, default=datetime.utcnow)

    pet = relationship("Pet", back_populates="applications")
    user = relationship("User", back_populates="applications")
