"""Enrutado principal del proyecto."""
import os

from django.contrib import admin
from django.urls import include, path

# La ruta del panel es configurable para no exponer la dirección habitual.
# Debe terminar en "/" (por ejemplo: "gestion-interna/").
ADMIN_URL = os.environ.get("DJANGO_ADMIN_URL", "admin/").strip().lstrip("/")
if not ADMIN_URL.endswith("/"):
    ADMIN_URL += "/"

urlpatterns = [
    path(ADMIN_URL, admin.site.urls),
    path("", include("portal.urls")),
]
