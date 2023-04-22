from core.apiv1.serializers import ChunkedUploadSerializer
from core.apiv1.utils import handle_chunked_file_model_association
from core.models import ChunkedUploadFile
from django.shortcuts import get_object_or_404
from drf_chunked_upload.views import ChunkedUploadView
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


class OfflineFileChunkedUploadView(ChunkedUploadView):
    model = ChunkedUploadFile
    serializer_class = ChunkedUploadSerializer
    permission_classes = (AllowAny,)

    # TODO: remove this after validating md5 hash
    do_checksum_check = False

    def _post(self, request, pk=None, *args, **kwargs) -> Response:
        chunked_upload = None
        if pk:
            upload_id = pk
        else:
            chunked_upload = self._put_chunk(request, *args, whole=True, **kwargs)
            upload_id = chunked_upload.id

        if not chunked_upload:
            chunked_upload = get_object_or_404(self.get_queryset(), pk=upload_id)

        self.is_valid_chunked_upload(chunked_upload)

        chunked_upload.completed()

        # after completion, move the uploaded file to the
        # uploaded file model.
        data = request.data
        object_id = data["object_id"]
        handle_chunked_file_model_association(chunked_upload, object_id)
        return Response({"data": "File Upload successful"}, status=status.HTTP_200_OK)
