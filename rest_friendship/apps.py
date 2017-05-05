# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import, print_function

from django.conf import settings
from django.apps import AppConfig


class RestFriendshipConfig(AppConfig):
    name = 'rest_friendship'
    verbose_name = "RestFriendship"

    @property
    def customized_settings(self):
        return getattr(settings, 'REST_FRIENDSHIP', {})

    @property
    def user_serializer(self):
        return self.customized_settings.get('USER_SERIALIZER', 'rest_friendship.serializers.UserSerializer')

    def ready(self):
        """Override this to put in:
            Users system checks
            Users signal registration
        """
        pass
