from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Report(Base):
    id = Column(Integer, primary_key=True, index=True)
    pet_name = Column(String, index=True)
    description = Column(String)
    location = Column(String)
    report_type = Column(String, default="lost") # lost, found
    status = Column(String, default="open")  # open, closed, resolved
    image_url = Column(String, nullable=True)
    contact_info = Column(String)
    user_id = Column(Integer, ForeignKey("user.id"))

    user = relationship("User", back_populates="reports")
