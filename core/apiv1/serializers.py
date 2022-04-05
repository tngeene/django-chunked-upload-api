from drf_chunked_upload.serializers import ChunkedUploadSerializer
from core.models import ChunkedUploadFile

class FileChunkedUploadSerializer(ChunkedUploadSerializer):
    viewname = 'cms:files:chunk_upload_files_part'

    class Meta:
        model = ChunkedUploadFile
        fields = '__all__'