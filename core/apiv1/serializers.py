from core.models import ChunkedUploadFile
from drf_chunked_upload import serializers as chunking_serializers

class ChunkedUploadSerializer(chunking_serializers.ChunkedUploadSerializer):
    viewname = 'core:api_v1:chunk_upload_files_part'

    class Meta:
        model = ChunkedUploadFile
        fields = '__all__'