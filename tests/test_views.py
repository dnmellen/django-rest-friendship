# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest
from rest_framework.test import APIClient
from rest_friendship.serializers import get_user_serializer, UserSerializer
from friendship.models import Friend, FriendshipRequest
from tests.serializers import TestUserSerializer

from .factories import UserFactory


def test_settings_user_serializer():
    assert get_user_serializer() == UserSerializer


def test_settings_user_serializer_with_specific_settings(settings):
    settings.REST_FRIENDSHIP = {
        'USER_SERIALIZER': 'tests.serializers.TestUserSerializer'
    }
    assert get_user_serializer() == TestUserSerializer


@pytest.mark.django_db
def test_list_friends():

    # Create users
    user1 = UserFactory()
    user2 = UserFactory()
    user3 = UserFactory()

    Friend.objects.add_friend(
        user2,                               # The sender
        user1,                               # The recipient
        message='Hi! I would like to add you'
    )

    Friend.objects.add_friend(
        user3,                               # The sender
        user1,                               # The recipient
        message='Hi! I would like to add you'
    )

    for friend_request in FriendshipRequest.objects.filter(to_user=user1):
        friend_request.accept()

    client = APIClient()
    client.force_authenticate(user=user1)
    response = client.get('/friends/')
    assert response.status_code == 200
    assert len(response.data) == 2
