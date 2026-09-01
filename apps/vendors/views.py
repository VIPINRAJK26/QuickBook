from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from .models import Vendor
from .serializers import VendorSerializer
from .services import VendorService


class VendorListCreateView(generics.ListCreateAPIView):
    serializer_class = VendorSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return Vendor.objects.all()

    def perform_create(self, serializer):
        VendorService.create_vendor(
            **serializer.validated_data
        )


class VendorUpdateView(generics.UpdateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [IsAdminUser]

    def perform_update(self, serializer):
        VendorService.update_vendor(
            vendor=serializer.instance,
            **serializer.validated_data,
        )