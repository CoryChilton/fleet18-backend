from rest_framework import routers
from .views import EventViewSet, ResultViewSet

router = routers.DefaultRouter()
router.register('events', EventViewSet, basename='events')
router.register('results', ResultViewSet, basename='results')

urlpatterns = router.urls