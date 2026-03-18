from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas
from app.api import deps

router = APIRouter()

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
    await db.refresh(report)
    return report

@router.get("/", response_model=List[schemas.Report])
async def read_reports(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    status: str = None,
) -> Any:
    """
    List all active reports.
    """
    query = select(models.Report).offset(skip).limit(limit)
    if status:
        query = query.where(models.Report.status == status)
    
    result = await db.execute(query)
    reports = result.scalars().all()
    return reports

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
    result = await db.execute(select(models.Report).where(models.Report.id == id))
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
    await db.refresh(report)
    return report
