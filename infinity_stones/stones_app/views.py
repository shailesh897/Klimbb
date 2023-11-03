from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Activation, Stone
from .serializers import ActivateRequestSerializer, ActivationSerializer
from django.utils import timezone
from celery.result import AsyncResult
from .tasks import process_stone_activation
from django.shortcuts import render


def index(request):
    return render(request, "stones_app/index.html")

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({'access_token': str(refresh.access_token)}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class ActivateView(APIView):
    @authentication_classes([IsAuthenticated])
    @permission_classes([IsAuthenticated])
    def post(self, request):
        serializer = ActivateRequestSerializer(data=request.data)
        if serializer.is_valid():
            stone_id = serializer.validated_data["stone_id"]
            user_id = serializer.validated_data["user_id"]
            power_duration = serializer.validated_data["power_duration"]

            existing_activation = Activation.objects.filter(
                user=user_id, stone=stone_id, end_time__gt=timezone.now()
            ).first()

            if existing_activation:
                return Response(
                    {"message": "Stone is already active for this user."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            active_activations = Activation.objects.filter(
                user=user_id, end_time__gt=timezone.now()
            )

            if active_activations:
                return Response(
                    {"message": "User already has an active stone activation."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            try:
                stone = Stone.objects.get(pk=stone_id)
                user = User.objects.get(pk=user_id)

                activation = Activation.objects.create(
                    user=user, stone=stone, power_duration=power_duration
                )

                # Trigger the Celery task to process the activation
                task = process_stone_activation.delay(activation.id)

                response_data = {
                    "message": "Activation in progress",
                    "task_id": task.id,
                }
                return Response(response_data, status=status.HTTP_202_ACCEPTED)

            except Stone.DoesNotExist:
                return Response(
                    {"message": "Stone not found"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            except User.DoesNotExist:
                return Response(
                    {"message": "User not found"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StoneStatusView(APIView):
    @authentication_classes([IsAuthenticated])
    @permission_classes([IsAuthenticated])
    def get(self, request, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(
                {"message": "User not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        activations = Activation.objects.filter(
            user=user, end_time__gt=timezone.now()
        )
        serializer = ActivationSerializer(activations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
