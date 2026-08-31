from rest_framework.permissions import BasePermission


class IsOwnerOrAdmin(BasePermission):
    """
    Allow users to access only their own referral data.
    Staff users can access any user's referral data.
    """

    def has_permission(self, request, view):
        user_id = view.kwargs.get("user_id")

        if request.user.is_staff:
            return True

        return request.user.id == user_id