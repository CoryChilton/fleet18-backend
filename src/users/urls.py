from rest_framework import routers
from .views import RacerViewSet

router = routers.DefaultRouter()
router.register('racers', RacerViewSet, basename='events')

urlpatterns = router.urls