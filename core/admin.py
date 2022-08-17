from django.contrib import admin

from core.models import ChunkedUploadFile, OfflineFile

# Register your models here.


admin.site.register(OfflineFile)
admin.site.register(ChunkedUploadFile)
