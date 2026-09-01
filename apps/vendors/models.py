from django.core.validators import RegexValidator
from django.db import models


phone_validator = RegexValidator(
    regex=r"^\+?[0-9]{10,15}$",
    message="Enter a valid phone number.",
)


class Vendor(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
    )

    email = models.EmailField(
        unique=True,
    )

    phone = models.CharField(
        max_length=16,
        validators=[phone_validator],
    )

    address = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return self.name