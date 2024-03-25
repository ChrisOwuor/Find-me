from django.conf import settings

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include("Users.urls")),
    path("app/stats/", include("Statistics.urls", )),
    path("", include("Api.urls", namespace="api")),



] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
