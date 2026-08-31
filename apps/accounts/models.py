import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)

    referral_code = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
    )

    class Meta:
        indexes = [
            models.Index(fields=["referral_code"]),
        ]

    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = self.generate_unique_referral_code()

        super().save(*args, **kwargs)

    @staticmethod
    def generate_unique_referral_code():
        while True:
            code = uuid.uuid4().hex[:10].upper()

            if not User.objects.filter(referral_code=code).exists():
                return code

    def __str__(self):
        return self.email