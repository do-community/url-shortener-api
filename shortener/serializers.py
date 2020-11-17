from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import URLRedirect


UserModel = get_user_model()


class URLRedirectSerializer(serializers.ModelSerializer):
    class Meta:
        model = URLRedirect
        fields = [
            "id",
            "short_link",
            "url",
            "visit_count",
        ]


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserModel
        # Tuple of serialized model fields (see link [2])
        fields = (
            "id",
            "username",
            "password",
        )
