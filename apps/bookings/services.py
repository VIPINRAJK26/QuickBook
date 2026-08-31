from django.db import transaction

from apps.events.models import Event

from .exceptions import (
    BookingAlreadyCancelledError,
    BookingPermissionError,
    InsufficientSeatsError,
)
from .models import Booking, BookingStatus


class BookingService:

    @staticmethod
    @transaction.atomic
    def create_booking(*, user, event, seats):
        """
        Create a booking safely and prevent overbooking.

        Acquires a row-level lock on the event to ensure that
        available_seats is re-read from the database inside the
        transaction, preventing concurrent overbooking.
        """

        event = Event.objects.select_for_update().get(pk=event.pk)

        if event.available_seats < seats:
            raise InsufficientSeatsError("Not enough seats available.")

        booking = Booking.objects.create(
            user=user,
            event=event,
            seats=seats,
            status=BookingStatus.CONFIRMED,
        )

        event.available_seats -= seats
        event.save(update_fields=["available_seats"])

        return booking

    @staticmethod
    @transaction.atomic
    def cancel_booking(*, booking_id, user):
        """
        Cancel a booking and restore seats to the event.

        Acquires row-level locks on both the booking and the event
        to prevent double seat restoration under concurrent
        cancellation requests.
        """

        try:
            booking = (
                Booking.objects
                .select_for_update()
                .select_related("event")
                .get(pk=booking_id)
            )
        except Booking.DoesNotExist:
            raise

        if booking.user_id != user.id:
            raise BookingPermissionError(
                "You do not have permission to cancel this booking."
            )

        if booking.status == BookingStatus.CANCELLED:
            raise BookingAlreadyCancelledError(
                "This booking has already been cancelled."
            )

        booking.status = BookingStatus.CANCELLED
        booking.save(update_fields=["status", "updated_at"])

        # Lock the event row before restoring seats to prevent
        # inconsistent available_seats under concurrent operations.
        event = Event.objects.select_for_update().get(pk=booking.event_id)
        event.available_seats += booking.seats
        event.save(update_fields=["available_seats"])

        # Refresh the booking's event reference so the returned
        # object reflects the updated seat count if needed.
        booking.event = event

        return booking