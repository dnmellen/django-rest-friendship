# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import include, url

urlpatterns = [
    url(r'^', include('rest_friendship.urls', namespace='rest_friendship')),
]
