import uuid
from django.db import models
from .utils import generate_chunked_filename, rename_blob, generate_offline_filename
from drf_chunked_upload.models import ChunkedUpload
from django.utils.translation import gettext_lazy as _
from django.core.files.uploadedfile import UploadedFile
from django.db import transaction
from django.utils import timezone
from drf_chunked_upload import settings as _settings
from .constants import FILE_TYPES


class CommonInfo(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)


# Create your models here.
class ChunkedUploadFile(ChunkedUpload):
    file = models.FileField(
        verbose_name=_("file"),
        max_length=255,
        upload_to=generate_chunked_filename,
        null=True,
    )

    def allowed_owners(self):
        return super(ChunkedUploadFile, self).allowed_owners()

    def allowed_owner(self, owner_type, owner_id=None, msg=None):
        return super(ChunkedUploadFile, self).allowed_owner(owner_type, owner_id, msg)

    def append_chunk(self, chunk, chunk_size=None, save=True):
        cloud_storage_file = self.file
        cloud_storage_file.close()
        cloud_storage_file.open(mode="w")
        for subchunk in chunk.chunks():
            cloud_storage_file.write(subchunk)
        if chunk_size is not None:
            self.offset += chunk_size
        elif hasattr(chunk, "size"):
            self.offset += chunk.size
        else:
            self.offset = self.file.size
        # clear any cached checksum
        self._checksum = None
        if save:
            self.save()
        self.file.close()

    def get_uploaded_file(self):
        cloud_storage_file = self.file
        cloud_storage_file.close()
        cloud_storage_file.open(mode="rb")
        return UploadedFile(file=self.file, name=self.filename, size=self.file.size)

    @transaction.atomic
    def completed(self, completed_at=timezone.now(), ext=_settings.COMPLETE_EXT):
        if ext != _settings.INCOMPLETE_EXT:
            original_path = self.file.name
            path_ext = original_path.split(".")[-1]
            # remove filename extension
            formatted_file_path = original_path.split(".")[0]
            self.file.name = formatted_file_path + ext
        self.status = self.COMPLETE
        self.completed_at = completed_at
        self.save()
        if ext != _settings.INCOMPLETE_EXT:
            rename_blob(original_path, self.file.name)
            self.save()


class OfflineFile(CommonInfo):
    file_type = models.CharField(
        max_length=30, choices=FILE_TYPES, null=True, blank=True
    )
    file = models.FileField(upload_to=generate_offline_filename, null=True, blank=True)
    file_url = models.URLField(null=True, blank=True, max_length=1000)
    unique_id = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
    description = models.TextField(null=True)

    def __str__(self) -> str:
        return f"{self.file}"
