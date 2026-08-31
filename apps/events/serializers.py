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