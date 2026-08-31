from rest_framework import serializers

from apps.events.models import Event

from .models import Booking


class BookingCreateSerializer(serializers.Serializer):
    event_id = serializers.PrimaryKeyRelatedField(
        source="event",
        queryset=Event.objects.all(),
    )

    seats = serializers.IntegerField(min_value=1)


class BookingSerializer(serializers.ModelSerializer):
    event_id = serializers.IntegerField(source="event.id", read_only=True)
    event_title = serializers.CharField(
        source="event.title",
        read_only=True,
    )

    class Meta:
        model = Booking
        fields = [
            "id",
            "event_id",
            "event_title",
            "seats",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "status",
            "created_at",
            "updated_at",
        ]