from fastapi import APIRouter

from app.api.v1.endpoints import auth, pets, upload, applications, reports, users

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(pets.router, prefix="/pets", tags=["pets"])
api_router.include_router(upload.router, prefix="/upload", tags=["upload"])
api_router.include_router(applications.router, prefix="/applications", tags=["applications"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
