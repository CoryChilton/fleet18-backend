from rest_framework import routers

from .views import NotificationPreferenceViewSet

router = routers.DefaultRouter()
router.register(
    "notification-preferences",
    NotificationPreferenceViewSet,
    basename="notification_preferences",
)

urlpatterns = router.urls
