from django.conf.urls import include, url

urlpatterns = [
    url('', include('rest_friendship.urls', namespace='rest_friendship')),
]
