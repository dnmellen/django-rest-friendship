# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import detail_route, list_route
from friendship.models import Friend, FriendshipRequest
from django.contrib.auth import get_user_model

from .serializers import get_user_serializer, FriendshipRequestSerializer


class FriendViewSet(viewsets.ViewSet):
    """
    ViewSet for Friend model
    """

    serializer_class = get_user_serializer()

    def list(self, request):
        friends = Friend.objects.friends(request.user)
        serializer = self.serializer_class(friends, many=True)
        return Response(serializer.data)

    @list_route()
    def requests(self, request):
        friend_requests = Friend.objects.unrejected_requests(user=request.user)
        return Response(FriendshipRequestSerializer(friend_requests, many=True).data)

    @list_route()
    def sent_requests(self, request):
        friend_requests = Friend.objects.sent_requests(user=request.user)
        return Response(FriendshipRequestSerializer(friend_requests, many=True).data)

    @list_route()
    def rejected_requests(self, request):
        friend_requests = Friend.objects.rejected_requests(user=request.user)
        return Response(FriendshipRequestSerializer(friend_requests, many=True).data)

    def create(self, request):
        """
        Creates a friend request

        POST data:
        - user_id
        - message
        """

        friend_obj = Friend.objects.add_friend(
            request.user,                                                     # The sender
            get_object_or_404(get_user_model(), pk=request.data['user_id']),  # The recipient
            message=request.data['message']
        )

        return Response(
            FriendshipRequestSerializer(friend_obj).data,
            status.HTTP_201_CREATED
        )


class FriendshipRequestViewSet(viewsets.ViewSet):
    """
    ViewSet for FriendshipRequest model
    """

    @detail_route(methods=['post'])
    def accept(self, request, pk=None):
        friendship_request = get_object_or_404(FriendshipRequest, pk=pk)
        friendship_request.accept()
        return Response(
            FriendshipRequestSerializer(friendship_request).data,
            status.HTTP_201_CREATED
        )

    @detail_route(methods=['post'])
    def reject(self, request, pk=None):
        friendship_request = get_object_or_404(FriendshipRequest, pk=pk)
        friendship_request.reject()
        return Response(
            FriendshipRequestSerializer(friendship_request).data,
            status.HTTP_201_CREATED
        )
