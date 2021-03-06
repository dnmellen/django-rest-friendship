# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('pk', 'username')
