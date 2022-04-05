from django.contrib import admin

from core.models import ChunkedUploadFile, OfflineFile

# Register your models here.


admin.register(OfflineFile)
admin.register(ChunkedUploadFile)
