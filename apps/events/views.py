from rest_framework import generics,status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .filters import EventFilter
from .models import Event
from .serializers import EventSerializer
from .permissions import IsStaffUser
from .services import EventService



class EventCreateView(generics.GenericAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsStaffUser]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        event = EventService.create_event(
            **serializer.validated_data
        )

        return Response(
            {
                "message": "Event created successfully.",
                "event": EventSerializer(event).data,
            },
            status=status.HTTP_201_CREATED,
        )


class EventListView(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Event.objects.order_by("start_time")

        return EventFilter.filter_queryset(
            queryset=queryset,
            params=self.request.query_params,
        )


class EventDetailView(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [AllowAny]


class EventUpdateView(generics.GenericAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsStaffUser]
    queryset = Event.objects.all()

    def patch(self, request, pk):
        event = self.get_object()

        serializer = self.get_serializer(
            event,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        event = EventService.update_event(
            event=event,
            **serializer.validated_data,
        )

        return Response(
            {
                "message": "Event updated successfully.",
                "event": EventSerializer(event).data,
            },
            status=status.HTTP_200_OK,
        )


class EventDeleteView(generics.GenericAPIView):
    permission_classes = [IsStaffUser]
    queryset = Event.objects.all()

    def delete(self, request, pk):
        event = self.get_object()
        event.delete()

        return Response(
            {
                "message": "Event deleted successfully."
            },
            status=status.HTTP_200_OK,
        )