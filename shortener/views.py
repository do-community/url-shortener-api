from django.shortcuts import redirect, get_object_or_404
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import viewsets
from .serializers import URLRedirectSerializer, UserSerializer
from .models import URLRedirect
from django.contrib.auth.models import User
import os


class index(generics.GenericAPIView):
    def get(self, request):
        if os.getenv("REDIRECT", "True") == "False":
            short_link = request.path.lstrip("/")
            print(short_link)
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


class RedirectViewset(viewsets.ModelViewSet):
    queryset = URLRedirect.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = URLRedirectSerializer


class UserViewset(viewsets.ModelViewSet):

    queryset = User.objects.all()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = UserSerializer
