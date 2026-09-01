from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView  # re-exported for urls.py
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from .serializers import RegisterSerializer, LoginSerializer, UserSerializer, LogoutSerializer
from .services import AccountService
from .throttles import RegisterRateThrottle,LoginRateThrottle


class RegisterView(APIView):
    throttle_classes = [RegisterRateThrottle]
    @extend_schema(request=RegisterSerializer, responses={201: dict, 400: dict})
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = AccountService.register_user(
            **serializer.validated_data
        )

        return Response(
            {
                "message": "User registered successfully.",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "referral_code": user.referral_code,
                },
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    throttle_classes = [LoginRateThrottle]
    @extend_schema(request=LoginSerializer, responses={200: dict, 400: dict})
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "message": "Login successful.",
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
            status=status.HTTP_200_OK,
        )


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses={200: UserSerializer})
    def get(self, request):
        serializer = UserSerializer(request.user)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(request=LogoutSerializer, responses={200: dict, 400: dict})
    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            AccountService.blacklist_refresh_token(
                serializer.validated_data["refresh"]
            )
        except ValueError as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {"message": "Logout successful. Refresh token has been blacklisted."},
            status=status.HTTP_200_OK,
        )
