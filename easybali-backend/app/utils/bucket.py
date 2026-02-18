from app.settings.config import settings
import boto3
import logging
import os
from botocore.exceptions import NoCredentialsError
from uuid import uuid4
from fastapi import HTTPException, UploadFile

logger = logging.getLogger(__name__)

AWS_ACCESS_KEY = settings.AWS_ACCESS_KEY
AWS_SECRET_KEY = settings.AWS_SECRET_KEY
AWS_BUCKET_NAME = settings.AWS_BUCKET_NAME
AWS_REGION = settings.AWS_REGION

# Lazy S3 client — only created on first use so a missing/empty AWS_REGION
# does NOT crash the app at import time (e.g. on Render dev deployments).
_s3_client = None


def _get_s3_client():
    global _s3_client
    if _s3_client is None:
        if not AWS_REGION:
            raise RuntimeError(
                "AWS_REGION is not configured. Set the AWS_REGION environment variable."
            )
        _s3_client = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY,
            region_name=AWS_REGION,
        )
    return _s3_client


async def upload_to_s3(file: UploadFile) -> str:
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"profile_image_{uuid4()}{file_extension}"
    try:
        _get_s3_client().upload_fileobj(
            file.file,
            AWS_BUCKET_NAME,
            unique_filename,
        )
        file_url = f"https://{AWS_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{unique_filename}"
        return file_url
    except NoCredentialsError:
        raise HTTPException(status_code=500, detail="Credentials not available")
    except RuntimeError as e:
        logger.warning(f"S3 not configured: {e}")
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


