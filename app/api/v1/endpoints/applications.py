from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas
from app.api import deps

router = APIRouter()

@router.post("/", response_model=schemas.Application)
async def create_application(
    *,
    db: AsyncSession = Depends(deps.get_db),
    application_in: schemas.ApplicationCreate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Submit an adoption application for a pet.
    """
    # Check if pet exists
    result = await db.execute(select(models.Pet).where(models.Pet.id == application_in.pet_id))
    pet = result.scalars().first()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")

    # Check if user already applied for this pet (optional but good practice)
    result = await db.execute(
        select(models.Application).where(
            models.Application.user_id == current_user.id,
            models.Application.pet_id == application_in.pet_id
        )
    )
    existing_application = result.scalars().first()
    if existing_application:
        raise HTTPException(status_code=400, detail="Application already exists for this pet")

    application = models.Application(
        pet_id=application_in.pet_id,
        user_id=current_user.id,
        message=application_in.message,
        status="pending"
    )
    db.add(application)
    await db.commit()
    await db.refresh(application)
    return application

@router.get("/", response_model=List[schemas.Application])
async def read_applications(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    List applications (User sees own, Admin/Shelter sees all).
    """
    if current_user.is_superuser:
        query = select(models.Application).offset(skip).limit(limit)
    else:
        query = select(models.Application).where(models.Application.user_id == current_user.id).offset(skip).limit(limit)
    
    result = await db.execute(query)
    applications = result.scalars().all()
    return applications

@router.put("/{id}", response_model=schemas.Application)
async def update_application(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: int,
    application_in: schemas.ApplicationUpdate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Update status (approve/reject). Only admin can update.
    """
    result = await db.execute(select(models.Application).where(models.Application.id == id))
    application = result.scalars().first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    # Only admin (superuser) can update status
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    if application_in.status:
        application.status = application_in.status
        
    db.add(application)
    await db.commit()
    await db.refresh(application)
    return application
