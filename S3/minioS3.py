from minio import Minio, S3Error
from io import BytesIO
from config import BaseConfigApp

from .base import Storage
from .exceptions import StogareUploadExcepion



class MinioStorage(Storage):
    def __init__(self, config:BaseConfigApp):
        self.client = Minio(
            endpoint=config.s3_endpoint,
            access_key=config.s3_access_key,
            secret_key=config.s3_secret_key,
            secure=False
        )
        self.bucket_name = config.s3_bucket_name


    def upload(self, filename:str, file_data:BytesIO, lenght:int, content_type:int):
        try:
            destination_file = f"upload/{filename}"

            if not self.client.bucket_exists(bucket_name=self.bucket_name):
                self.client.make_bucket(bucket_name=self.bucket_name)

            self.client.put_object(
                bucket_name=self.bucket_name,
                object_name=destination_file,
                data=file_data,
                length=lenght,
                content_type=content_type
            )

            url = self.client.presigned_get_object(
                bucket_name=self.bucket_name,
                object_name=destination_file
            )

            return url
        except S3Error:
            raise StogareUploadExcepion(
               f"Failed to upload file: {filename}"
            )