# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import, print_function

from django.conf import settings
from django.apps import AppConfig
from .utils import import_from_string


class RestFriendshipConfig(AppConfig):
    name = 'rest_friendship'
    verbose_name = "RestFriendship"

    @property
    def customized_settings(self):
        return getattr(settings, 'REST_FRIENDSHIP', {})

    @property
    def user_serializer(self):
        return import_from_string(
            self.customized_settings.get(
                'USER_SERIALIZER',
                'rest_friendship.serializers.UserSerializer'
            ),
            'USER_SERIALIZER'
        )

    @property
    def permission_classes(self):
        classes = self.customized_settings.get(
            'PERMISSION_CLASSES',
            ('rest_framework.permissions.IsAuthenticated',)
        )

        return [
            import_from_string(c, 'PERMISSION_CLASSES')
            for c in classes
        ]

    def ready(self):
        """Override this to put in:
            Users system checks
            Users signal registration
        """
        pass
