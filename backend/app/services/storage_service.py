import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
from pathlib import Path
from typing import Optional
import logging
from ..config import settings

logger = logging.getLogger(__name__)

class StorageService:
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            endpoint_url=settings.S3_ENDPOINT,
            aws_access_key_id=settings.S3_ACCESS_KEY,
            aws_secret_access_key=settings.S3_SECRET_KEY,
            config=Config(signature_version='s3v4'),
            region_name=settings.S3_REGION
        )
        self.bucket_name = settings.S3_BUCKET_NAME
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self):
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
        except ClientError:
            try:
                self.s3_client.create_bucket(Bucket=self.bucket_name)
                logger.info(f"Created bucket: {self.bucket_name}")
            except ClientError as e:
                logger.warning(f"Could not create bucket: {e}")

    def upload_file(self, file_path: str, object_name: str) -> str:
        """Upload file to S3 and return URL"""
        try:
            self.s3_client.upload_file(
                file_path,
                self.bucket_name,
                object_name,
                ExtraArgs={'ACL': 'public-read'}
            )
            url = f"{settings.S3_ENDPOINT}/{self.bucket_name}/{object_name}"
            return url
        except ClientError as e:
            logger.error(f"Upload failed: {e}")
            raise

    def download_file(self, object_name: str, file_path: str):
        """Download file from S3"""
        try:
            self.s3_client.download_file(self.bucket_name, object_name, file_path)
        except ClientError as e:
            logger.error(f"Download failed: {e}")
            raise

    def get_presigned_url(self, object_name: str, expiration: int = 3600) -> str:
        """Generate presigned URL for temporary access"""
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': object_name},
                ExpiresIn=expiration
            )
            return url
        except ClientError as e:
            logger.error(f"Presigned URL generation failed: {e}")
            raise

    def delete_file(self, object_name: str):
        """Delete file from S3"""
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=object_name)
        except ClientError as e:
            logger.error(f"Delete failed: {e}")
            raise

storage_service = StorageService()
