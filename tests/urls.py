from django.urls import path, include

urlpatterns = [
    path('', include(('rest_friendship.urls', 'rest_friendship'), namespace='rest_friendship')),
]
