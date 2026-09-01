from django.urls import path

from .views import (
    DashboardEventCreateView,
    DashboardEventListView,
    DashboardEventUpdateView,
    DashboardStatsView,
    DashboardUserDetailView,
    DashboardUserListView,
    DashboardUserReferralTreeView,
    DashboardVendorListCreateView,
    DashboardVendorUpdateView,
)


urlpatterns = [
    path("", DashboardStatsView.as_view(), name="dashboard-stats"),
    path("users/", DashboardUserListView.as_view(), name="dashboard-user-list"),
    path("users/<int:pk>/", DashboardUserDetailView.as_view(), name="dashboard-user-detail"),
    path("users/<int:pk>/referral-tree/", DashboardUserReferralTreeView.as_view(), name="dashboard-user-referral-tree"),
    path("vendors/", DashboardVendorListCreateView.as_view(), name="dashboard-vendor-list-create"),
    path("vendors/<int:pk>/update/", DashboardVendorUpdateView.as_view(), name="dashboard-vendor-update"),
    path("events/", DashboardEventListView.as_view(), name="dashboard-event-list"),
    path("events/create/", DashboardEventCreateView.as_view(), name="dashboard-event-create"),
    path("events/<int:pk>/update/", DashboardEventUpdateView.as_view(), name="dashboard-event-update"),
]