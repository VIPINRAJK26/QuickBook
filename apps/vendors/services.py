from .models import Vendor


class VendorService:

    @staticmethod
    def create_vendor(**validated_data):
        return Vendor.objects.create(**validated_data)

    @staticmethod
    def update_vendor(*, vendor, **validated_data):
        for field, value in validated_data.items():
            setattr(vendor, field, value)

        vendor.save(update_fields=list(validated_data.keys()) + ["updated_at"])

        return vendor