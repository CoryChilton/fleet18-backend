from rest_framework import routers

from .views import AnnouncementViewSet

router = routers.DefaultRouter()
router.register("announcements", AnnouncementViewSet, basename="announcements")

urlpatterns = router.urls
