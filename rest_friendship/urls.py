# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from .views import FriendViewSet, FriendshipRequestViewSet

from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'friends', FriendViewSet, base_name='friends')
router.register(r'friendrequests', FriendshipRequestViewSet, base_name='friendrequests')
urlpatterns = router.urls
