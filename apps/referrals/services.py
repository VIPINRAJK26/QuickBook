from collections import deque

from django.db import transaction

from .models import ReferralNode, ReferralPosition


class ReferralService:

    @staticmethod
    def create_root_node(*, user):
        """Create a referral node for a user without a referrer."""

        return ReferralNode.objects.create(
            user=user,
            referrer=None,
            parent=None,
            position=None,
        )

    @staticmethod
    def place_user(*, user, referrer):
        """
        Place a user in the referrer's binary tree using breadth-first,
        left-to-right placement.
        """

        root_node = ReferralNode.objects.select_for_update().get(
            user=referrer
        )

        queue = deque([root_node])

        while queue:
            current_node = queue.popleft()

            children = {
                child.position: child
                for child in current_node.children.all()
            }

            if ReferralPosition.LEFT not in children:
                return ReferralNode.objects.create(
                    user=user,
                    referrer=referrer,
                    parent=current_node,
                    position=ReferralPosition.LEFT,
                )

            if ReferralPosition.RIGHT not in children:
                return ReferralNode.objects.create(
                    user=user,
                    referrer=referrer,
                    parent=current_node,
                    position=ReferralPosition.RIGHT,
                )

            queue.append(children[ReferralPosition.LEFT])
            queue.append(children[ReferralPosition.RIGHT])

        raise RuntimeError("Unable to find an available referral position.")