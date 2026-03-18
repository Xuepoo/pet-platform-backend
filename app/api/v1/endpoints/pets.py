from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Pet])
async def read_pets(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    species: Optional[str] = None,
    breed: Optional[str] = None,
    status: Optional[str] = "available",
) -> Any:
    """
    Retrieve pets.
    """
    query = select(models.Pet)
    if species:
        query = query.where(models.Pet.species == species)
    if breed:
        query = query.where(models.Pet.breed == breed)
    if status:
        query = query.where(models.Pet.status == status)
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    pets = result.scalars().all()
    return pets


@router.post("/", response_model=schemas.Pet)
async def create_pet(
    *,
    db: AsyncSession = Depends(deps.get_db),
    pet_in: schemas.PetCreate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Create new pet.
    """
    pet_data = pet_in.dict()
    pet = models.Pet(**pet_data, owner_id=current_user.id)
    db.add(pet)
    await db.commit()
    await db.refresh(pet)
    return pet


@router.get("/{pet_id}", response_model=schemas.Pet)
async def read_pet(
    *,
    db: AsyncSession = Depends(deps.get_db),
    pet_id: int,
) -> Any:
    """
    Get pet by ID.
    """
    result = await db.execute(select(models.Pet).where(models.Pet.id == pet_id))
    pet = result.scalars().first()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    return pet


@router.put("/{pet_id}", response_model=schemas.Pet)
async def update_pet(
    *,
    db: AsyncSession = Depends(deps.get_db),
    pet_id: int,
    pet_in: schemas.PetUpdate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Update a pet.
    """
    result = await db.execute(select(models.Pet).where(models.Pet.id == pet_id))
    pet = result.scalars().first()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    if pet.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    
    update_data = pet_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(pet, field, value)
    
    db.add(pet)
    await db.commit()
    await db.refresh(pet)
    return pet


@router.delete("/{pet_id}", response_model=schemas.Pet)
async def delete_pet(
    *,
    db: AsyncSession = Depends(deps.get_db),
    pet_id: int,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Delete a pet.
    """
    result = await db.execute(select(models.Pet).where(models.Pet.id == pet_id))
    pet = result.scalars().first()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    if pet.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    
    await db.delete(pet)
    await db.commit()
    return pet
