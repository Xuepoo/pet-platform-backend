from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.core.config import settings
from app.models.user import User as UserModel
from app.schemas.user import User as UserSchema
from app.schemas.user import UserUpdate

router = APIRouter()


@router.put("/me", response_model=UserSchema)
async def update_user_me(
    *,
    db: AsyncSession = Depends(deps.get_db),
    user_in: UserUpdate,
    current_user: UserModel = Depends(deps.get_current_user),
) -> Any:
    """
    Update own user.
    """
    user_data = user_in.model_dump(exclude_unset=True)
    for field in user_data:
        setattr(current_user, field, user_data[field])

    db.add(current_user)
    await db.commit()
    await db.refresh(current_user)
    return current_user


@router.get("/", response_model=List[UserSchema])
async def read_users(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: UserModel = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve users.
    """
    result = await db.execute(select(UserModel).offset(skip).limit(limit))
    users = result.scalars().all()
    return users


@router.put("/{user_id}", response_model=UserSchema)
async def update_user(
    *,
    db: AsyncSession = Depends(deps.get_db),
    user_id: int,
    user_in: UserUpdate,
    current_user: UserModel = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a user.
    """
    result = await db.execute(select(UserModel).where(UserModel.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    user_data = jsonable_encoder(user)
    update_data = user_in.dict(exclude_unset=True)
    for field in user_data:
        if field in update_data:
            setattr(user, field, update_data[field])
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@router.delete("/{user_id}", response_model=UserSchema)
async def delete_user(
    *,
    db: AsyncSession = Depends(deps.get_db),
    user_id: int,
    current_user: UserModel = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Delete a user.
    """
    result = await db.execute(select(UserModel).where(UserModel.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    await db.delete(user)
    await db.commit()
    return user
