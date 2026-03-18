from typing import Any
from fastapi import APIRouter, File, UploadFile, HTTPException
from app.core.config import settings
from app.core.storage import minio_client
import uuid
import io

router = APIRouter()

@router.post("/", response_model=dict)
async def upload_image(
    file: UploadFile = File(...)
) -> Any:
    """
    Upload an image to Minio storage.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    try:
        # Read file content
        content = await file.read()
        file_size = len(content)
        file_data = io.BytesIO(content)

        # Generate unique filename
        filename_ext = file.filename.split(".")[-1]
        filename = f"{uuid.uuid4()}.{filename_ext}"

        # Upload
        minio_client.put_object(
            bucket_name=settings.MINIO_BUCKET_NAME,
            object_name=filename,
            data=file_data,
            length=file_size,
            content_type=file.content_type
        )

        # Construct URL
        protocol = "https" if settings.MINIO_SECURE else "http"
        url = f"{protocol}://{settings.MINIO_ENDPOINT}/{settings.MINIO_BUCKET_NAME}/{filename}"
        
        return {"url": url, "filename": filename}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not upload file: {str(e)}")
