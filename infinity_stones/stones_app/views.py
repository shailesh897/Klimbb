from datetime import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Activation, Stone
from .serializers import ActivationSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView

from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User
from rest_framework.exceptions import NotFound
from .serializers import LoginRequestSerializer, ActivateRequestSerializer
from .tasks import process_stone_activation


class LoginView(APIView):
    def post(self, request):
        serializer = LoginRequestSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]

            user = authenticate(username=username, password=password)

            if user:
                refresh = RefreshToken.for_user(user)
                return Response(
                    {
                        "data": {
                            "refresh": str(refresh),
                            "access": str(refresh.access_token),
                        }
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                raise AuthenticationFailed("Invalid username or password")
        else:
            return Response(
                {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )


class ActivateView(APIView):
    def post(self, request):
        serializer = ActivateRequestSerializer(data=request.data)

        if serializer.is_valid():
            stone_id = serializer.validated_data["stone_id"]
            user_id = serializer.validated_data["user_id"]
            power_duration = serializer.validated_data["power_duration"]

            try:
                stone = Stone.objects.get(id=stone_id)
                user = User.objects.get(id=user_id)

                activation = Activation.objects.create(
                    user=user, stone=stone, power_duration=power_duration
                )

                # Trigger the Celery task to process the activation
                process_stone_activation.delay(activation.id)

                response_data = {
                    "message": "Activation in progress",
                }
                return Response(response_data, status=status.HTTP_202_ACCEPTED)

            except (Stone.DoesNotExist, User.DoesNotExist):
                raise NotFound("Stone or User not found")

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
