from app.settings.config import settings
import boto3
import os
from botocore.exceptions import NoCredentialsError
from uuid import uuid4
from fastapi import HTTPException, UploadFile



AWS_ACCESS_KEY = settings.AWS_ACCESS_KEY
AWS_SECRET_KEY = settings.AWS_SECRET_KEY
AWS_BUCKET_NAME = settings.AWS_BUCKET_NAME
AWS_REGION = settings.AWS_REGION
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)



async def upload_to_s3(file: UploadFile) -> str:
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"profile_image_{uuid4()}{file_extension}"
    try:
        s3_client.upload_fileobj(
            file.file,
            AWS_BUCKET_NAME,
            unique_filename,
        )
        file_url = f"https://{AWS_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{unique_filename}"
        return file_url
    except NoCredentialsError:
        raise HTTPException(status_code=500, detail="Credentials not available")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

