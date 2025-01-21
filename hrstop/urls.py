from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from ninja import NinjaAPI
from .utils.auth import *
from user.views import *
from employee.views import *
from settings.general_settings.views import setting_api

api = NinjaAPI(auth=AsyncJWTAuth())
api.add_router('employee', employee_api)
api.add_router('user', user_api)
api.add_router('settings', setting_api)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)