from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from ninja import NinjaAPI
from .utils.auth import *
from employee.views import *
from user.views import *
from settings.general_settings.views import *
from settings.employee_settings.views import *

api = NinjaAPI(auth=AsyncJWTAuth())
api.add_router('employee', employee_api)
api.add_router('user', user_api)
api.add_router('general_settings', general_setting_api)
api.add_router('employee_settings', employee_setting_api)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)