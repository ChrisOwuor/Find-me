from django.conf import settings

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include("Users.urls", namespace='blog_api')),
    path("app/",include("Note.urls",namespace="notes")),
    path("",include("Api.urls",namespace="api")),



]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

