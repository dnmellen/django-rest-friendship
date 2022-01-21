from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'user_id', 'username', 'email')

