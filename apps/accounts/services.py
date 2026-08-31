from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError


User = get_user_model()


class AccountService:

    @staticmethod
    def register_user(validated_data):
        referral_code = validated_data.pop("referral_code", None)

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
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