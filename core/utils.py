from django.conf import settings
from django.shortcuts import get_object_or_404
from drf_chunked_upload import settings as _settings
from core.models import OfflineFile

bucket_name = settings.DEFAULT_STORAGE.get("BUCKET_NAME")
storage = settings.DEFAULT_STORAGE.get("STORAGE")


def generate_chunked_filename(instance: object, filename: str) -> str:
    ext = _settings.INCOMPLETE_EXT
    filename = str(instance.id) + ext
    file_url = f"tmp/files/chunked_uploads/{filename}"
    return file_url


def rename_blob(blob_name, new_name):
    """Renames a blob."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The ID of the GCS object to rename
    # blob_name = "your-object-name"
    # The new ID of the GCS object
    # new_name = "new-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    new_blob = bucket.rename_blob(blob, new_name)
    return new_blob


def handle_chunked_file_model_association(chunked_upload, object_id: int):
    offline_file_to_update = get_object_or_404(OfflineFile, id=object_id)
    if offline_file_to_update.file:
        offline_file_to_update.file.delete()
    offline_file_to_update.file = chunked_upload.get_uploaded_file()
    offline_file_to_update.save()


def generate_offline_filename(instance, filename: str) -> str:
    ext = filename.split(".")[-1]
    name = f"{instance.unique_id}.{ext}"
    url = f"files/{instance.file_type}/{instance.id}/{name}"
    return url
