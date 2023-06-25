from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register(r"google-login", views.GoogleLogin, basename="google-login")
router.register(r"me", views.Profile)
router.register(r"user-stats", views.StatsViewSet)
appname = "users"
urlpatterns = router.urls
