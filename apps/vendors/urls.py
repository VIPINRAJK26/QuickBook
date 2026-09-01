
from django.urls import path

from .views import VendorListCreateView, VendorUpdateView

urlpatterns = [
    path("", VendorListCreateView.as_view(), name="vendor-list-create"),
    path("<int:pk>/update/", VendorUpdateView.as_view(), name="vendor-update"),
]