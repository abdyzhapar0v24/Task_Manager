from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.views.generic import RedirectView


schema_view = get_schema_view(
    openapi.Info(
        title="Task Manager API",
        default_version="v1",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # редирект с /
    path('', RedirectView.as_view(url='/pages/tasks/', permanent=False)),

    path('admin/', admin.site.urls),
    path('api/', include('tasks.urls_api')),

    # ⬅️ ВАЖНО: подключаем ОДИН РАЗ
    path('', include('tasks.urls')),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0)),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0)),


]
