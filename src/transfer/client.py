import os
from google.oauth2.service_account import Credentials
from google.cloud import storage
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class GoogleCloudStorageClient:
    cred = Credentials.from_service_account_info(
        {
            "type": "service_account",
            "project_id": os.environ.get("GCP_PROJECT_ID"),
            "private_key_id": os.environ.get("GCS_PRIVATE_KEY_ID"),
            "private_key": os.environ.get("GCS_PRIVATE_KEY").replace("\\n", "\n"),
            "client_email": os.environ.get("GCS_CLIENT_EMAIL"),
            "client_id": os.environ.get("GCS_CLIENT_ID"),
            "auth_uri": os.environ.get("GCS_AUTH_URI"),
            "token_uri": os.environ.get("GCS_TOKEN_URI"),
            "auth_provider_x509_cert_url": os.environ.get(
                "GCS_AUTH_PROVIDER_X509_CERT_URL"
            ),
            "client_x509_cert_url": os.environ.get("GCS_CLIENT_X509_CERT_URL"),
        }
    )
    client = storage.Client(credentials=cred)

    @classmethod
    def _create_bucket_instance(cls, bucket_name: str, destination_blob_name: str):
        bucket = cls.client.bucket(bucket_name)
        return bucket.blob(destination_blob_name)

    @classmethod
    def upload_file(
        cls, bucket_name: str, destination_blob_name: str, local_file_path: str
    ) -> None:
        blob = cls._create_bucket_instance(bucket_name, destination_blob_name)
        blob.upload_from_filename(local_file_path)
