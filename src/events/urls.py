from rest_framework import routers
from .views import EventViewSet, ResultViewSet, RaceViewSet

router = routers.DefaultRouter()
router.register('events', EventViewSet, basename='events')
router.register('results', ResultViewSet, basename='results')
router.register('races', RaceViewSet, basename='race')

urlpatterns = router.urls