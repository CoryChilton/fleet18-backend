from django.contrib.auth import login
from django.utils import timezone
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from rest_framework import generics, permissions, viewsets
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

from events.models import Result
from events.serializers import ResultSerializer
from notifications.models import NotificationPreference
from notifications.serializers import NotificationPreferenceSerializer

from .models import Racer, User
from .serializers import (
    LoginSerializer,
    RacerSerializer,
    RegisterSerializer,
    UserSerializer,
)


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        login(request, user)
        token = AuthToken.objects.create(user)[1]
        return Response(
            {
                "user": UserSerializer(user).data,
                "token": token,
            }
        )


class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        # print(request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        return super(LoginView, self).post(request, format=None)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint for users.
    """

    queryset = User.objects.all()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = UserSerializer

    # @action(detail=True, methods=["get"], url_path="notification-preferences")
    # def notification_preferences(self, request, pk=None):
    #     user = self.get_object()
    #     prefs = NotificationPreference.objects.filter(user=user)
    #     serializer = NotificationPreferenceSerializer(prefs, many=True)
    #     return Response(serializer.data)


class RacerViewSet(viewsets.ModelViewSet):
    """
    API endpoint for racers.
    """

    queryset = Racer.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RacerSerializer

    @action(detail=True, methods=["get"], url_path="results")
    def results(self, request, pk=None):
        racer = self.get_object()
        results = Result.objects.filter(racer=racer)
        serializer = ResultSerializer(results, many=True)
        return Response(serializer.data)
