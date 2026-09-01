from django.contrib.auth import get_user_model
from django.db.models import Q

from apps.referrals.models import ReferralNode, ReferralPosition


User = get_user_model()


class DashboardService:

    @staticmethod
    def get_user_referral_tree(*, user_id, search_query=None):
        """
        Build the referral subtree rooted at the given user.

        If search_query is provided, each node in the returned tree
        includes a ``matched`` boolean flag indicating whether it
        matches (case-insensitive partial match on username, email,
        or referral_code).  The full tree is always returned so that
        the frontend can preserve parent-child context.

        Returns:
            dict – nested tree structure.

        Raises:
            ReferralNode.DoesNotExist – if the user has no referral node.
        """

        # 1. Fetch root node for the target user.
        root_node = ReferralNode.objects.select_related("user").get(
            user_id=user_id,
        )

        # 2. Fetch ALL nodes in one query with their users.
        #    We build a children_map in a single O(n) pass, then
        #    traverse only the subtree rooted at root_node during
        #    tree construction — nodes outside the subtree are never
        #    visited.
        all_nodes = ReferralNode.objects.select_related("user").all()

        children_map = {}
        for node in all_nodes:
            if node.parent_id is not None:
                children_map.setdefault(node.parent_id, []).append(node)

        # 3. Build the nested tree, optionally annotating with search.
        search_lower = search_query.lower().strip() if search_query else None

        def build_node(node):
            children = {
                child.position: build_node(child)
                for child in children_map.get(node.id, [])
            }

            result = {
                "user_id": node.user.id,
                "username": node.user.username,
                "email": node.user.email,
                "referral_code": node.user.referral_code,
                "position": node.position,
                "children": {
                    "left": children.get(ReferralPosition.LEFT),
                    "right": children.get(ReferralPosition.RIGHT),
                },
            }

            if search_lower is not None:
                result["matched"] = (
                    search_lower in node.user.username.lower()
                    or search_lower in node.user.email.lower()
                    or search_lower in node.user.referral_code.lower()
                )

            return result

        return build_node(root_node)
