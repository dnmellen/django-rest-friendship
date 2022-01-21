
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from friendship.models import Friend, FriendshipRequest
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response
from .serializers import FriendshipRequestSerializer, FriendSerializer, FriendshipRequestResponseSerializer
from django.utils.module_loading import import_string


User = get_user_model()


REST_FRIENDSHIP = getattr(settings, "REST_FRIENDSHIP", None)
PERMISSION_CLASSES = [import_string(c)
                      for c in REST_FRIENDSHIP["PERMISSION_CLASSES"]]
USER_SERIALIZER = import_string(REST_FRIENDSHIP["USER_SERIALIZER"])


class FriendViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Friend model
    """
    permission_classes = PERMISSION_CLASSES
    serializer_class = None

    def list(self, request):
        friend_requests = Friend.objects.friends(user=request.user)
        self.queryset = friend_requests
        self.http_method_names = ['get', 'head', 'options']
        return Response(FriendSerializer(friend_requests, many=True).data)

    @ action(detail=False)
    def requests(self, request):
        friend_requests = Friend.objects.unrejected_requests(user=request.user)
        self.queryset = friend_requests
        return Response(FriendshipRequestSerializer(friend_requests, many=True).data)

    @ action(detail=False)
    def sent_requests(self, request):
        friend_requests = Friend.objects.sent_requests(user=request.user)
        self.queryset = friend_requests
        return Response(FriendshipRequestSerializer(friend_requests, many=True).data)

    @ action(detail=False)
    def rejected_requests(self, request):
        friend_requests = Friend.objects.rejected_requests(user=request.user)
        self.queryset = friend_requests
        return Response(FriendshipRequestSerializer(friend_requests, many=True).data)

    @ action(detail=False, serializer_class=FriendshipRequestSerializer, methods=['post'])
    def add_friend(self, request, username=None):
        """
        Add a new friend with the post form below.
        """
        try:
            # Creates a friend request from POST data:
            # - username and/or email
            # - message
            username = request.data.get('to_user', '')
            friend_obj = Friend.objects.add_friend(
                # The sender
                request.user,
                # The recipient
                get_object_or_404(
                    User, username=username),
                # Message (...or empty str)
                message=request.data.get('message', '')
            )
            return Response(
                FriendshipRequestSerializer(friend_obj).data,
                status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {'message': str(e)},
                status.HTTP_400_BAD_REQUEST
            )

    @ action(detail=False, serializer_class=FriendSerializer, methods=['post'])
    def remove_friend(self, request, id=None, username=None):
        """
        Deletes a friend relationship

        The user id specified in the URL will be removed from the current user's friends
        """
        try:
            id = request.data.get('id', None)
            username = request.data['username']

            user_friend = get_object_or_404(
                User, pk=id, username=username)

            if Friend.objects.remove_friend(request.user, user_friend):
                message = 'deleted'
                status_code = status.HTTP_204_NO_CONTENT
            else:
                message = 'not deleted'
                status_code = status.HTTP_304_NOT_MODIFIED

            return Response(
                {"message": message},
                status=status_code
            )
        except Exception as e:
            return Response(
                {'message': str(e)},
                status.HTTP_400_BAD_REQUEST
            )

    @ action(detail=False, serializer_class=FriendshipRequestResponseSerializer, methods=['post'])
    def accept_request(self, request, id=None):
        """
        Accepts a friend request

        The request id specified in the URL will be accepted
        """
        try:
            id = request.data.get('id', None)
            friend_requests = Friend.objects.unrejected_requests(
                user=request.user)
            self.queryset = friend_requests
            friendship_request = get_object_or_404(
                FriendshipRequest, pk=id, to_user=request.user)

            friendship_request.accept()
            return Response(
                {"message": "Request accepted, user added to friends."},
                status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {'message': str(e)},
                status.HTTP_400_BAD_REQUEST
            )

    @ action(detail=False, serializer_class=FriendshipRequestResponseSerializer, methods=['post'])
    def reject_request(self, request, id=None):
        """
        Rejects a friend request

        The request id specified in the URL will be rejected
        """
        try:
            id = request.data.get('id', None)
            friend_requests = Friend.objects.rejected_requests(
                user=request.user)
            self.queryset = friend_requests
            friendship_request = get_object_or_404(
                FriendshipRequest, pk=id, to_user=request.user)
            friendship_request.reject()
            return Response(
                FriendshipRequestSerializer(friendship_request).data,
                status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {'message': str(e)},
                status.HTTP_400_BAD_REQUEST
            )
