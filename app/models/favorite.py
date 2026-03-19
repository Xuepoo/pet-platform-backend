from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class PetFavorite(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    pet_id = Column(Integer, ForeignKey("pet.id"))

    user = relationship("User", back_populates="favorites")
    pet = relationship("Pet", back_populates="favorited_by")
