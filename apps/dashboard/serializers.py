from django.contrib.auth import get_user_model

from rest_framework import serializers


User = get_user_model()


class DashboardUserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "referral_code",
            "date_joined",
        ]


class DashboardUserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "referral_code",
            "date_joined",
            "is_active",
        ]