from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("api/v1/users/", include("users.urls"), name="users"),
    path("api/v1/files/", include("main.urls"), name="files"),
    path("admin/", admin.site.urls),
]
