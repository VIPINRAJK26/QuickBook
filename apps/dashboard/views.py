from django.http import Http404
from rest_framework import generics, status
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from django.contrib.auth import get_user_model

from apps.bookings.models import Booking
from apps.events.filters import EventFilter
from apps.events.models import Event
from apps.events.serializers import EventSerializer
from apps.events.services import EventService
from apps.referrals.models import ReferralNode
from apps.vendors.models import Vendor
from apps.vendors.serializers import VendorSerializer
from apps.vendors.services import VendorService

from .serializers import DashboardUserDetailSerializer, DashboardUserListSerializer
from .services import DashboardService


User = get_user_model()


class DashboardStatsView(APIView):
    permission_classes = [IsAdminUser]

    @extend_schema(responses={200: dict})
    def get(self, request):
        data = {
            "total_customers": User.objects.filter(
                is_staff=False
            ).count(),

            "total_vendors": Vendor.objects.count(),

            "total_events": Event.objects.count(),

            "total_bookings": Booking.objects.count(),
        }

        return Response(data)


class DashboardUserListView(generics.ListAPIView):
    serializer_class = DashboardUserListSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [SearchFilter]
    search_fields = [
        "username",
        "email",
        "referral_code",
    ]

    def get_queryset(self):
        return User.objects.filter(
            is_staff=False
        ).order_by("-date_joined")


class DashboardUserDetailView(generics.RetrieveAPIView):
    """
    Staff-only endpoint to view detailed information about one customer.
    Staff users are excluded from the queryset (customer management only).
    """
    serializer_class = DashboardUserDetailSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return User.objects.filter(is_staff=False)


class DashboardUserReferralTreeView(APIView):
    """
    Staff-only endpoint returning the referral tree rooted at a customer.

    Supports ``?search=<term>`` to annotate each node with a ``matched``
    flag (case-insensitive partial match on username, email, referral_code).
    The full tree is always returned to preserve parent-child context.
    """
    permission_classes = [IsAdminUser]

    @extend_schema(responses={200: dict, 404: dict})
    def get(self, request, pk):
        # Ensure the target user is a customer (is_staff=False).
        if not User.objects.filter(pk=pk, is_staff=False).exists():
            raise Http404("Customer not found.")

        search_query = request.query_params.get("search", "").strip() or None

        try:
            tree = DashboardService.get_user_referral_tree(
                user_id=pk,
                search_query=search_query,
            )
        except ReferralNode.DoesNotExist:
            raise Http404("Referral node not found for this customer.")

        return Response(tree, status=status.HTTP_200_OK)


class DashboardVendorListCreateView(generics.ListCreateAPIView):
    """
    Staff-only vendor list (with search and pagination) and creation.
    Delegates creation to VendorService from the vendors app.
    """
    serializer_class = VendorSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [SearchFilter]
    search_fields = [
        "name",
        "email",
        "phone",
    ]

    def get_queryset(self):
        return Vendor.objects.all()

    def perform_create(self, serializer):
        VendorService.create_vendor(
            **serializer.validated_data
        )


class DashboardVendorUpdateView(generics.UpdateAPIView):
    """
    Staff-only vendor update (PUT/PATCH).
    Delegates update to VendorService from the vendors app.
    """
    serializer_class = VendorSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return Vendor.objects.all()

    def perform_update(self, serializer):
        VendorService.update_vendor(
            vendor=serializer.instance,
            **serializer.validated_data,
        )


class DashboardEventListView(generics.ListAPIView):
    """
    Staff-only event list with search and location filtering.

    Supports:
        ?search=<term>    — searches title, description, location
        ?location=<term>  — filters by location specifically

    Uses the existing EventFilter from the events app.
    Paginated via global StandardResultsSetPagination.
    """
    serializer_class = EventSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        queryset = Event.objects.order_by("start_time")

        return EventFilter.filter_queryset(
            queryset=queryset,
            params=self.request.query_params,
        )


class DashboardEventCreateView(generics.GenericAPIView):
    """
    Staff-only event creation.
    Delegates to EventService.create_event() which sets
    available_seats = total_seats automatically.
    """
    serializer_class = EventSerializer
    permission_classes = [IsAdminUser]

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


class DashboardEventUpdateView(generics.GenericAPIView):
    """
    Staff-only event update (PATCH).
    Delegates to EventService.update_event() from the events app.
    """
    serializer_class = EventSerializer
    permission_classes = [IsAdminUser]
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