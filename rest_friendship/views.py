
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.utils.module_loading import import_string
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from friendship.models import Friend, FriendshipRequest
from friendship.exceptions import AlreadyExistsError, AlreadyFriendsError
from .serializers import FriendshipRequestSerializer, FriendSerializer, FriendshipRequestResponseSerializer


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
    serializer_class = USER_SERIALIZER
    lookup_field = 'pk'

    def list(self, request):
        friend_requests = Friend.objects.friends(user=request.user)
        self.queryset = friend_requests
        self.http_method_names = ['get', 'head', 'options', ]
        return Response(FriendSerializer(friend_requests, many=True).data)

    def retrieve(self, request, pk=None):
        self.queryset = Friend.objects.friends(user=request.user)
        requested_user = get_object_or_404(User, pk=pk)
        if Friend.objects.are_friends(request.user, requested_user):
            self.http_method_names = ['get', 'head', 'options', ]
            return Response(FriendSerializer(requested_user, many=False).data)
        else:
            return Response(
                {'message': "Friend relationship not found for user."},
                status.HTTP_400_BAD_REQUEST
            )

    @ action(detail=False)
    def requests(self, request):
        friend_requests = Friend.objects.unrejected_requests(user=request.user)
        self.queryset = friend_requests
        return Response(
            FriendshipRequestSerializer(friend_requests, many=True).data)

    @ action(detail=False)
    def sent_requests(self, request):
        friend_requests = Friend.objects.sent_requests(user=request.user)
        self.queryset = friend_requests
        return Response(
            FriendshipRequestSerializer(friend_requests, many=True).data)

    @ action(detail=False)
    def rejected_requests(self, request):
        friend_requests = Friend.objects.rejected_requests(user=request.user)
        self.queryset = friend_requests
        return Response(
            FriendshipRequestSerializer(friend_requests, many=True).data)

    @ action(detail=False,
             serializer_class=FriendshipRequestSerializer,
             methods=['post'])
    def add_friend(self, request, username=None):
        """
        Add a new friend with POST data
        - to_user
        - message
        """
        # Creates a friend request from POST data:
        # - username
        # - message
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        to_user = get_object_or_404(
            User,
            username=serializer.validated_data.get('to_user')
        )

        try:
            friend_obj = Friend.objects.add_friend(
                # The sender
                request.user,
                # The recipient
                to_user,
                # Message (...or empty str)
                message=request.data.get('message', '')
            )
            return Response(
                FriendshipRequestSerializer(friend_obj).data,
                status.HTTP_201_CREATED
            )
        except (AlreadyExistsError, AlreadyFriendsError) as e:
            return Response(
                {"message": str(e)},
                status.HTTP_400_BAD_REQUEST
            )

    @ action(detail=False, serializer_class=FriendshipRequestSerializer, methods=['post'])
    def remove_friend(self, request):
        """
        Deletes a friend relationship.

        The username specified in the POST data will be
        removed from the current user's friends.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        to_user = get_object_or_404(
            User,
            username=serializer.validated_data.get('to_user')
        )

        if Friend.objects.remove_friend(request.user, to_user):
            message = 'Friend deleted.'
            status_code = status.HTTP_204_NO_CONTENT
        else:
            message = 'Friend not found.'
            status_code = status.HTTP_400_BAD_REQUEST

        return Response(
            {"message": message},
            status=status_code
        )

    @ action(detail=False,
             serializer_class=FriendshipRequestResponseSerializer,
             methods=['post'])
    def accept_request(self, request, id=None):
        """
        Accepts a friend request

        The request id specified in the URL will be accepted
        """
        id = request.data.get('id', None)
        friendship_request = get_object_or_404(
            FriendshipRequest, pk=id)

        if not friendship_request.to_user == request.user:
            return Response(
                {"message": "Request for current user not found."},
                status.HTTP_400_BAD_REQUEST
            )

        friendship_request.accept()
        return Response(
            {"message": "Request accepted, user added to friends."},
            status.HTTP_201_CREATED
        )

    @ action(detail=False,
             serializer_class=FriendshipRequestResponseSerializer,
             methods=['post'])
    def reject_request(self, request, id=None):
        """
        Rejects a friend request

        The request id specified in the URL will be rejected
        """
        id = request.data.get('id', None)
        friendship_request = get_object_or_404(
            FriendshipRequest, pk=id)
        if not friendship_request.to_user == request.user:
            return Response(
                {"message": "Request for current user not found."},
                status.HTTP_400_BAD_REQUEST
            )

        friendship_request.reject()

        return Response(
            {
                "message": "Request rejected, user NOT added to friends."
            },
            status.HTTP_201_CREATED
        )
