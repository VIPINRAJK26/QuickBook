from rest_framework import serializers

from .models import Vendor


class VendorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vendor
        fields = [
            "id",
            "name",
            "email",
            "phone",
            "address",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]