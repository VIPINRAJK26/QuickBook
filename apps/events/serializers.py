from rest_framework import serializers

from .models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "description",
            "location",
            "start_time",
            "end_time",
            "total_seats",
            "available_seats",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "available_seats",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):
        start_time = attrs.get(
            "start_time",
            getattr(self.instance, "start_time", None),
        )

        end_time = attrs.get(
            "end_time",
            getattr(self.instance, "end_time", None),
        )

        if start_time and end_time and end_time <= start_time:
            raise serializers.ValidationError(
                {
                    "end_time": (
                        "End time must be later than start time."
                    )
                }
            )

        return attrs