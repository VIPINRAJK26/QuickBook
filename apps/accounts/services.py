from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.db import transaction
from apps.referrals.models import ReferralNode
from apps.referrals.services import ReferralService


User = get_user_model()


class AccountService:

    @staticmethod
    @transaction.atomic
    def register_user(*, username, email, password, referral_code=None):

        # Find the referrer BEFORE creating the user.
        referrer = None

        if referral_code:
            referrer = User.objects.filter(
                referral_code=referral_code
            ).first()

            if referrer is None:
                raise ValueError("Invalid referral code.")

        # Create the user using Django's password hashing.
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )

        # User registered without a referral code.
        if referrer is None:
            ReferralService.create_root_node(user=user)

        # User registered using a referral code.
        else:
            ReferralService.place_user(
                user=user,
                referrer=referrer,
            )

        return user

    @staticmethod
    def blacklist_refresh_token(raw_token: str) -> None:
        """
        Validate and blacklist a refresh token.

        Raises ValueError with a human-readable message for any token
        problem (invalid, expired, already blacklisted, malformed).
        """
        try:
            token = RefreshToken(raw_token)
            token.blacklist()
        except TokenError as exc:
            raise ValueError(str(exc)) from exc