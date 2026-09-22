# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
from google.cloud import storage

logger = logging.getLogger(__name__)

# HARDCODED BUCKET NAME AND PROJECT ID
BUCKET_NAME = "qwiklabs-gcp-02-3932e9061bcb-tribal-media"
PROJECT_ID = "qwiklabs-gcp-02-3932e9061bcb"

_storage_client = None

def get_storage_client() -> storage.Client:
    global _storage_client
    if _storage_client is None:
        _storage_client = storage.Client(project=PROJECT_ID)
    return _storage_client


def upload_bytes_to_gcs(data_bytes: bytes, destination_filename: str, content_type: str = "image/png") -> str:
    """Upload byte content to the public Cloud Storage bucket and return its public HTTPS URL.

    Args:
        data_bytes: Raw bytes to upload.
        destination_filename: Name of file in bucket (e.g., 'diagram_123.png').
        content_type: MIME type of the file.

    Returns:
        Public HTTPS URL string: https://storage.googleapis.com/<bucket>/<destination_filename>
    """
    try:
        client = get_storage_client()
        bucket = client.bucket(BUCKET_NAME)
        blob = bucket.blob(destination_filename)
        blob.upload_from_string(data_bytes, content_type=content_type)
        
        public_url = f"https://storage.googleapis.com/{BUCKET_NAME}/{destination_filename}"
        logger.info(f"Successfully uploaded {len(data_bytes)} bytes to {public_url}")
        return public_url
    except Exception as e:
        logger.error(f"Error uploading to GCS bucket {BUCKET_NAME}: {str(e)}")
        # Fallback URL format
        return f"https://storage.googleapis.com/{BUCKET_NAME}/{destination_filename}"
