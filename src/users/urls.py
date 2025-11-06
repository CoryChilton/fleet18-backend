from django.urls import path
from knox import views as knox_views
from rest_framework import routers

from .views import LoginView, RacerViewSet, RegisterView, UserViewSet

router = routers.DefaultRouter()
router.register("racers", RacerViewSet, basename="events")
router.register("users", UserViewSet, basename="users")

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", LoginView.as_view(), name="knox_login"),
    path("auth/logout/", knox_views.LogoutView.as_view(), name="knox_logout"),
    path("auth/logoutall/", knox_views.LogoutAllView.as_view(), name="knox_logoutall"),
] + router.urls
