from django.contrib.auth import get_user_model
from rest_framework import serializers

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ["username", "name", "url"]

        extra_kwargs = {
            "url": {"view_name": "rest:user-detail", "lookup_field": "username"},
        }
