from rest_framework import serializers

from .models import ReferralNode


class ReferralTreeNodeSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user.id")
    username = serializers.CharField(source="user.username")
    referral_code = serializers.CharField(source="user.referral_code")

    class Meta:
        model = ReferralNode
        fields = [
            "user_id",
            "username",
            "referral_code",
            "position",
        ]


class ReferralRootSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user.id")
    username = serializers.CharField(source="user.username")
    email = serializers.EmailField(source="user.email")
    referral_code = serializers.CharField(source="user.referral_code")

    class Meta:
        model = ReferralNode
        fields = [
            "user_id",
            "username",
            "email",
            "referral_code",
        ]


class ReferralStatsSerializer(serializers.Serializer):
    left_team_count = serializers.IntegerField()
    right_team_count = serializers.IntegerField()