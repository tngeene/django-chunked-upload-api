
from core.apiv1.views import OfflineFileChunkedUploadView
from django.urls import path

app_name = 'api_v1'

urlpatterns = [
    path('chunk-upload/',
         OfflineFileChunkedUploadView.as_view(),
         name='chunk_upload_files'),
    path('chunk-upload/<uuid:pk>',
         OfflineFileChunkedUploadView.as_view(),
         name='chunk_upload_files_part')
]
