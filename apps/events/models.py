from django.core.validators import MinValueValidator
from django.db import models


class Event(models.Model):
    title = models.CharField(max_length=255)

    description = models.TextField(
        blank=True,
    )

    location = models.CharField(max_length=255)

    start_time = models.DateTimeField()

    end_time = models.DateTimeField()

    total_seats = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    available_seats = models.PositiveIntegerField(
        validators=[MinValueValidator(0)]
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["start_time"]

        indexes = [
            models.Index(fields=["start_time"]),
            models.Index(fields=["location"]),
        ]

        constraints = [
            models.CheckConstraint(
                condition=models.Q(end_time__gt=models.F("start_time")),
                name="event_end_after_start",
            ),
            models.CheckConstraint(
                condition=models.Q(
                    available_seats__lte=models.F("total_seats")
                ),
                name="available_seats_not_exceed_total",
            ),
        ]

    def __str__(self):
        return self.title