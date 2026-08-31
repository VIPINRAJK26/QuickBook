from collections import deque

from django.contrib.auth import get_user_model
from django.db.models import Prefetch

from .models import ReferralNode, ReferralPosition


User = get_user_model()


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

    @staticmethod
    def get_node(*, user_id):
        """
        Return the referral node for a user.
        """

        return ReferralNode.objects.select_related(
            "user",
            "referrer",
            "parent",
            "parent__user",
        ).get(user_id=user_id)

    @staticmethod
    def get_root(*, user_id):
        """
        Find the root node by walking up the parent chain.
        """

        node = ReferralService.get_node(user_id=user_id)

        while node.parent_id is not None:
            node = ReferralNode.objects.select_related(
                "user",
                "parent",
            ).get(pk=node.parent_id)

        return node

    @staticmethod
    def get_tree(*, user_id):
        """
        Return the complete referral subtree rooted at the given user.
        """

        root_node = ReferralNode.objects.select_related("user").get(
            user_id=user_id
        )

        nodes = ReferralNode.objects.select_related("user").all()

        children_map = {}

        for node in nodes:
            if node.parent_id is not None:
                children_map.setdefault(node.parent_id, []).append(node)

        return root_node, children_map

    @staticmethod
    def get_team_stats(*, user_id):
        """
        Return total descendants in the user's left and right teams.
        """

        root_node = ReferralNode.objects.get(user_id=user_id)

        children = {
            child.position: child
            for child in root_node.children.all()
        }

        left_count = 0
        right_count = 0

        if ReferralPosition.LEFT in children:
            left_count = ReferralService._count_subtree(
                children[ReferralPosition.LEFT]
            )

        if ReferralPosition.RIGHT in children:
            right_count = ReferralService._count_subtree(
                children[ReferralPosition.RIGHT]
            )

        return {
            "left_team_count": left_count,
            "right_team_count": right_count,
        }

    @staticmethod
    def _count_subtree(root_node):
        """
        Count a node and all of its descendants.
        """

        count = 0
        queue = deque([root_node])

        while queue:
            current_node = queue.popleft()
            count += 1

            children = current_node.children.all()

            queue.extend(children)

        return count

    @staticmethod
    def build_tree(*, root_node, children_map):
        """
        Build a nested tree structure without additional database queries.
        """
    
        def build_node(node):
            children = {
                child.position: build_node(child)
                for child in children_map.get(node.id, [])
            }
    
            return {
                "user_id": node.user.id,
                "username": node.user.username,
                "referral_code": node.user.referral_code,
                "position": node.position,
                "children": {
                    "left": children.get(ReferralPosition.LEFT),
                    "right": children.get(ReferralPosition.RIGHT),
                },
            }
    
        return build_node(root_node)