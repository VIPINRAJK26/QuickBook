from django.conf import settings
from django.db import models


class ReferralPosition(models.TextChoices):
    LEFT = "left", "Left"
    RIGHT = "right", "Right"


class ReferralNode(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="referral_node",
    )

    referrer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="direct_referrals",
    )

    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children",
    )

    position = models.CharField(
        max_length=5,
        choices=ReferralPosition.choices,
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["parent", "position"],
                name="unique_referral_position_per_parent",
            ),
        ]
        indexes = [
            models.Index(fields=["parent", "position"]),
            models.Index(fields=["referrer"]),
        ]

    def __str__(self):
        return f"{self.user.username} referral node"