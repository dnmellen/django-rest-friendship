# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

from django.apps import apps
from django.contrib.auth import get_user_model
from rest_framework import serializers
from friendship.models import FriendshipRequest
from .utils import import_from_string

config = apps.get_app_config('rest_friendship')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('pk', 'username', 'email')


class FriendshipRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendshipRequest
        fields = ('id', 'from_user', 'to_user', 'message', 'created', 'rejected', 'viewed')


def get_user_serializer():
    return import_from_string(config.user_serializer, 'USER_SERIALIZER')
