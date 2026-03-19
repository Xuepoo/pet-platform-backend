from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app import models, schemas
from app.api import deps
from app.schemas.report import ReportAuthor

router = APIRouter()


def report_to_response(report: models.Report) -> schemas.Report:
    """Convert Report model to Report schema with author info."""
    author = None
    if report.user:
        author = ReportAuthor(
            id=report.user.id,
            full_name=report.user.full_name,
            avatar=report.user.avatar
        )
    return schemas.Report(
        id=report.id,
        pet_name=report.pet_name,
        description=report.description,
        location=report.location,
        report_type=report.report_type,
        status=report.status,
        image_url=report.image_url,
        contact_info=report.contact_info,
        user_id=report.user_id,
        created_at=report.created_at,
        updated_at=report.updated_at,
        author=author
    )


@router.post("/", response_model=schemas.Report)
async def create_report(
    *,
    db: AsyncSession = Depends(deps.get_db),
    report_in: schemas.ReportCreate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Create a lost/found report.
    """
    report = models.Report(
        pet_name=report_in.pet_name,
        description=report_in.description,
        location=report_in.location,
        report_type=report_in.report_type,
        contact_info=report_in.contact_info,
        user_id=current_user.id,
        status="open"
    )
    db.add(report)
    await db.commit()
    await db.refresh(report, ["user"])
    return report_to_response(report)


@router.get("/", response_model=List[schemas.Report])
async def read_reports(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    status: str = None,
) -> Any:
    """
    List all active reports with author info.
    """
    query = select(models.Report).options(
        selectinload(models.Report.user)
    ).order_by(models.Report.created_at.desc()).offset(skip).limit(limit)
    
    if status:
        query = query.where(models.Report.status == status)
    
    result = await db.execute(query)
    reports = result.scalars().all()
    return [report_to_response(r) for r in reports]


@router.get("/{id}", response_model=schemas.Report)
async def read_report(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    Get a single report by ID with author info.
    """
    result = await db.execute(
        select(models.Report)
        .options(selectinload(models.Report.user))
        .where(models.Report.id == id)
    )
    report = result.scalars().first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report_to_response(report)


@router.put("/{id}", response_model=schemas.Report)
async def update_report(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: int,
    report_in: schemas.ReportUpdate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Update report status (e.g., mark as resolved).
    Only the owner of the report or a superuser can update it.
    """
    result = await db.execute(
        select(models.Report)
        .options(selectinload(models.Report.user))
        .where(models.Report.id == id)
    )
    report = result.scalars().first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    if not current_user.is_superuser and report.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    if report_in.status is not None:
        report.status = report_in.status
    if report_in.report_type is not None:
        report.report_type = report_in.report_type
    if report_in.image_url is not None:
        report.image_url = report_in.image_url
    if report_in.description is not None:
        report.description = report_in.description
    if report_in.location is not None:
        report.location = report_in.location
    if report_in.contact_info is not None:
        report.contact_info = report_in.contact_info
    if report_in.pet_name is not None:
        report.pet_name = report_in.pet_name

    db.add(report)
    await db.commit()
    await db.refresh(report, ["user"])
    return report_to_response(report)


@router.delete("/{id}", status_code=204)
async def delete_report(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_user),
) -> None:
    """
    Delete a report.
    Only the owner of the report or a superuser can delete it.
    """
    result = await db.execute(select(models.Report).where(models.Report.id == id))
    report = result.scalars().first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    if not current_user.is_superuser and report.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    await db.delete(report)
    await db.commit()
