"""Pet model for adoption management.

This module defines the Pet SQLAlchemy model with relationships
to owners and adoption applications.
"""

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Pet(Base):
    """Pet model for animals available for adoption.
    
    Attributes:
        id: Primary key.
        name: Pet's name.
        species: Type of animal (dog, cat, bird, etc.).
        breed: Specific breed.
        age: Age in years.
        description: Detailed description of the pet.
        status: Adoption status (available, adopted, pending).
        owner_id: Foreign key to the user who listed the pet.
        owner: Relationship to the owner user.
        applications: Relationship to adoption applications.
    """
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    species = Column(String, index=True)
    breed = Column(String, index=True)
    age = Column(Integer)
    description = Column(String)
    status = Column(String, default="available")
    owner_id = Column(Integer, ForeignKey("user.id"))

    owner = relationship("User", back_populates="pets")
    applications = relationship("Application", back_populates="pet")
