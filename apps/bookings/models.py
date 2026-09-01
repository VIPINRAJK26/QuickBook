from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class BookingStatus(models.TextChoices):
    CONFIRMED = "confirmed", "Confirmed"
    CANCELLED = "cancelled", "Cancelled"


class Booking(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookings",
    )

    event = models.ForeignKey(
        "events.Event",
        on_delete=models.PROTECT,
        related_name="bookings",
    )

    seats = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    status = models.CharField(
        max_length=20,
        choices=BookingStatus.choices,
        default=BookingStatus.CONFIRMED,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["user", "status"]),
            models.Index(fields=["event", "status"]),
        ]

    def __str__(self):
        return f"Booking #{self.pk} - {self.user} - {self.event}"