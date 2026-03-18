from typing import Optional

from pydantic import BaseModel, ConfigDict


class PetBase(BaseModel):
    name: Optional[str] = None
    species: Optional[str] = None
    breed: Optional[str] = None
    age: Optional[int] = None
    description: Optional[str] = None
    status: Optional[str] = "available"  # available, adopted, pending


class PetCreate(PetBase):
    name: str
    species: str
    breed: str
    age: int
    description: str


class PetUpdate(PetBase):
    pass


class PetInDBBase(PetBase):
    id: int
    owner_id: int
    model_config = ConfigDict(from_attributes=True)


class Pet(PetInDBBase):
    pass


class PetInDB(PetInDBBase):
    pass
