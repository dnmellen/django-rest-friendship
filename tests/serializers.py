# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

from django.apps import apps
from django.contrib.auth import get_user_model
from rest_framework import serializers


class TestUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('pk', 'username')
