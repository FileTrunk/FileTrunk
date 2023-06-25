from django.db.models import base
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register(
    r"share-load",
    views.FileSharingViewSet,
    basename="file-sharing",
)
router.register(
    r"file-load", views.FileUploadViewSet, basename="upload-download"
)
router.register(
    r"download", views.DownloadInitializationViewSet, basename="download-add"
)
router.register(r"", views.FileSystemViewSet, basename="file-system")
appname = "main"
urlpatterns = router.urls
