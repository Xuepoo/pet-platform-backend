"""Pet Platform FastAPI application entry point.

This module creates and configures the FastAPI application instance
with middleware, routers, and lifecycle management.
"""

from contextlib import asynccontextmanager
import json

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.storage import minio_client
from app.api.api import api_router
from app.core.logging import setup_logging

setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle events.
    
    Handles startup tasks like ensuring the MinIO bucket exists
    and setting up public read access policy.
    
    Args:
        app: The FastAPI application instance.
    
    Yields:
        None
    """
    try:
        if not minio_client.bucket_exists(settings.MINIO_BUCKET_NAME):
            minio_client.make_bucket(settings.MINIO_BUCKET_NAME)
            policy = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": {"AWS": ["*"]},
                        "Action": ["s3:GetObject"],
                        "Resource": [f"arn:aws:s3:::{settings.MINIO_BUCKET_NAME}/*"]
                    }
                ]
            }
            minio_client.set_bucket_policy(
                settings.MINIO_BUCKET_NAME, json.dumps(policy)
            )
            print(f"Created bucket {settings.MINIO_BUCKET_NAME}")
    except Exception as e:
        print(f"Warning: Could not initialize Minio bucket: {e}")
    yield


def create_app() -> FastAPI:
    """Create and configure the FastAPI application.
    
    Sets up CORS middleware and includes API routers.
    
    Returns:
        Configured FastAPI application instance.
    """
    app = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        lifespan=lifespan
    )

    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router, prefix=settings.API_V1_STR)

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
