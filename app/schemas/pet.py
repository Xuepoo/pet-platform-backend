from typing import Optional

from pydantic import BaseModel, ConfigDict


class PetBase(BaseModel):
    name: Optional[str] = None
    species: Optional[str] = None
    breed: Optional[str] = None
    age: Optional[int] = None
    description: Optional[str] = None
    status: Optional[str] = "available"  # available, adopted, pending
    gender: Optional[str] = None
    size: Optional[str] = None
    image_url: Optional[str] = None


class PetCreate(PetBase):
    name: str
    species: str
    breed: str
    age: int
    description: str
    gender: str
    size: str
    image_url: Optional[str] = None


class PetUpdate(PetBase):
    pass


class PetInDBBase(PetBase):
    id: int
    owner_id: Optional[int] = None
    model_config = ConfigDict(from_attributes=True)


class Pet(PetInDBBase):
    is_favorited: bool = False


class PetInDB(PetInDBBase):
    pass
