from rest_framework import serializers
from .models import URLRedirect


class URLRedirectSerializer(serializers.ModelSerializer):
    class Meta:
        model = URLRedirect
        fields = [
            "short_link",
            "url",
        ]