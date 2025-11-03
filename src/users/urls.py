from rest_framework import routers

from .views import RacerViewSet, UserViewSet

router = routers.DefaultRouter()
router.register("racers", RacerViewSet, basename="events")
router.register("users", UserViewSet, basename="users")

urlpatterns = router.urls
