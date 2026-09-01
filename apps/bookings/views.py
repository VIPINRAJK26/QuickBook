from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from .exceptions import (
    BookingAlreadyCancelledError,
    BookingPermissionError,
    InsufficientSeatsError,
)
from .models import Booking
from .serializers import BookingCreateSerializer, BookingSerializer
from .services import BookingService
from .throttles import BookingRateThrottle


class BookingListCreateView(generics.ListAPIView):
    """
    GET  /api/bookings/     → List the authenticated user's bookings.
    POST /api/bookings/     → Create a new booking.

    Combines list and create on the same path because Django URL
    routing does not dispatch by HTTP method. The list behaviour
    is provided by ListAPIView; the POST handler is added manually
    to keep the view thin, following the project's existing pattern.
    """

    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [BookingRateThrottle]

    def get_queryset(self):
        return (
            Booking.objects
            .filter(user=self.request.user)
            .select_related("event")
            .order_by("-created_at")
        )

    @extend_schema(request=BookingCreateSerializer, responses={201: BookingSerializer, 400: dict})
    def post(self, request):
        serializer = BookingCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            booking = BookingService.create_booking(
                user=request.user,
                **serializer.validated_data,
            )
        except InsufficientSeatsError as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "message": "Booking created successfully.",
                "booking": BookingSerializer(booking).data,
            },
            status=status.HTTP_201_CREATED,
        )


class BookingCancelView(generics.GenericAPIView):
    """
    POST /api/bookings/<id>/cancel/

    Cancels a confirmed booking and restores the seats to the event.

    Uses POST rather than PATCH because this is a discrete action/command,
    not a general-purpose partial update. This prevents clients from
    setting arbitrary fields and matches the project's existing
    action-style endpoints (e.g. POST /api/auth/login/).
    """

    permission_classes = [IsAuthenticated]

    @extend_schema(request=None, responses={200: BookingSerializer, 400: dict, 403: dict, 404: dict})
    def post(self, request, pk):
        try:
            booking = BookingService.cancel_booking(
                booking_id=pk,
                user=request.user,
            )
        except Booking.DoesNotExist:
            return Response(
                {"detail": "Booking not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except BookingPermissionError as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_403_FORBIDDEN,
            )
        except BookingAlreadyCancelledError as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "message": "Booking cancelled successfully.",
                "booking": BookingSerializer(booking).data,
            },
            status=status.HTTP_200_OK,
        )
