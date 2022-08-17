from django.urls import path, include

app_name = 'core'

urlpatterns = [
    path('v1/', include('core.apiv1.urls'))
]