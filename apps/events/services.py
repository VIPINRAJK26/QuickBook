from .models import Event


class EventService:

    @staticmethod
    def create_event(**validated_data):
        total_seats = validated_data["total_seats"]

        return Event.objects.create(
            **validated_data,
            available_seats=total_seats,
        )

    @staticmethod
    def update_event(*, event, **validated_data):
        for field, value in validated_data.items():
            setattr(event, field, value)

        event.save()

        return event