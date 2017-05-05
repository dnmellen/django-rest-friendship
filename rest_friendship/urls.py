# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.conf.urls import url

from .views import FriendViewSet

from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'friends', FriendViewSet, base_name='friends')
urlpatterns = router.urls
