from django.http import Http404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    ReferralRootSerializer,
    ReferralStatsSerializer,
)
from .services import ReferralService
from .models import ReferralNode

class ReferralTreeView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            root_node, children_map = ReferralService.get_tree(
                user_id=user_id
            )
        except ReferralNode.DoesNotExist:
            raise Http404("User referral node not found.")

        tree = ReferralService.build_tree(
            root_node=root_node,
            children_map=children_map,
        )

        return Response(tree, status=status.HTTP_200_OK)


class ReferralRootView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            root_node = ReferralService.get_root(user_id=user_id)
        except ReferralNode.DoesNotExist:
            raise Http404("User referral node not found.")

        serializer = ReferralRootSerializer(root_node)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class ReferralStatsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            stats = ReferralService.get_team_stats(
                user_id=user_id
            )
        except ReferralNode.DoesNotExist:
            raise Http404("User referral node not found.")

        serializer = ReferralStatsSerializer(stats)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )