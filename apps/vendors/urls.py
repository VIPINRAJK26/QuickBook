
from django.urls import path

from .views import VendorListCreateView, VendorUpdateView

urlpatterns = [
    path("vendors/", VendorListCreateView.as_view(), name="vendor-list-create"),
    path("vendors/<int:pk>/", VendorUpdateView.as_view(), name="vendor-update"),
]