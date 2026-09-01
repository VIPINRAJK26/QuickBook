from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser

from apps.accounts.models import User
from apps.bookings.models import Booking
from apps.events.models import Event
from apps.vendors.models import Vendor


class DashboardStatsView(APIView):
    permission_classes = [IsAdminUser]

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