from django.shortcuts import redirect, get_object_or_404
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import viewsets
from .serializers import URLRedirectSerializer, UserSerializer
from .models import URLRedirect
from django.contrib.auth.models import User
from django.conf import settings
import os
import re


class index(APIView):
    def get(self, request):
        if settings.FORCE_SCRIPT_NAME:
            regex_str = "^\/{0}\/?".format(settings.FORCE_SCRIPT_NAME.lstrip("/"))
        else:
            regex_str = "/"
        short_link = re.sub(regex_str, "", request.path)

        print(short_link)

        if os.getenv("REDIRECT", "True") == "False":
            redir = get_object_or_404(URLRedirect, short_link=short_link)
            redir.visit_count = redir.visit_count + 1
            redir.save()
            return Response({"redirect": redir.url})
        else:
            short_link = request.path.lstrip("/")
            redir = get_object_or_404(URLRedirect, short_link=short_link)
            redir.visit_count = redir.visit_count + 1
            redir.save()
            return redirect(redir.url)


class IsCreationOrIsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            if view.action == "create":
                return True
            else:
                return False
        else:
            return True


class RedirectViewset(viewsets.ModelViewSet):
    queryset = URLRedirect.objects.all()

    if os.getenv("ALLOW_OPEN_ACCESS", "False") == "True":
        permission_classes = [IsCreationOrIsAuthenticated]
    else:
        permission_classes = [permissions.IsAuthenticated]

    serializer_class = URLRedirectSerializer


class UserViewset(viewsets.ModelViewSet):

    queryset = User.objects.all()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = UserSerializer
