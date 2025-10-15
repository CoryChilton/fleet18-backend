from rest_framework import routers
from .views import EventPhotoViewSet

router = routers.DefaultRouter()
router.register('event-photos', EventPhotoViewSet, basename='event_photos')

urlpatterns = router.urls