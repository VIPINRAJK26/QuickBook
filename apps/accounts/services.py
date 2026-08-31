from django.contrib.auth import get_user_model


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