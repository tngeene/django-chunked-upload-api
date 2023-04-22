
from core.models import OfflineFile
from django.shortcuts import get_object_or_404


def handle_chunked_file_model_association(chunked_upload, object_id: int) -> None:
    offline_file_to_update = get_object_or_404(OfflineFile, id=object_id)
    breakpoint()
    if offline_file_to_update.file:
        offline_file_to_update.file.delete()
    offline_file_to_update.file = chunked_upload.get_uploaded_file()
    offline_file_to_update.save()