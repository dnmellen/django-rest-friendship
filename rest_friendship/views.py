# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from rest_framework import viewsets
from rest_framework.response import Response
from friendship.models import Friend

from .serializers import get_user_serializer


class FriendViewSet(viewsets.ViewSet):
    """
    ViewSet for Friend model
    """

    serializer_class = get_user_serializer()

    def list(self, request):
        friends = Friend.objects.friends(request.user)
        serializer = self.serializer_class(friends, many=True)
        return Response(serializer.data)

