from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Pet(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    species = Column(String, index=True)
    breed = Column(String, index=True)
    age = Column(Integer)
    description = Column(String)
    status = Column(String, default="available")  # available, adopted, pending
    owner_id = Column(Integer, ForeignKey("user.id"))

    owner = relationship("User", back_populates="pets")
    applications = relationship("Application", back_populates="pet")
