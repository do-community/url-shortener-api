from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import URLRedirectSerializer
from django.forms.models import model_to_dict
from .models import URLRedirect
import os


class index(APIView):
    def get(self, request):
        if os.getenv("REDIRECT", "True") == "False":
            short_link = request.path.lstrip("/")
            redir = get_object_or_404(URLRedirect, short_link=short_link)
            return Response({"redirect": redir.url})
        else:
            short_link = request.path.lstrip("/")
            redir = get_object_or_404(URLRedirect, short_link=short_link)
            redir.visit_count = redir.visit_count + 1
            redir.save()
            return redirect(redir.url)


class redir_admin(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        urls = URLRedirect.objects.all()
        urls_list = [model_to_dict(x) for x in urls]
        return Response(urls_list, 200)

    def post(self, request):
        url_redirect = URLRedirectSerializer(data=request.data)

        if url_redirect.is_valid() is True:
            url_redirect.save()
            return Response({"message": "Redirect successfully added"})
        else:
            return Response({"message": url_redirect.errors}, 422)

    def delete(self, request, short_link):
        redir = get_object_or_404(URLRedirect, short_link=short_link)
        redir.delete()
        return Response({"message": "Redirect successfully deleted"})

    def put(self, request):
        short_link = request.data.get("short_link", None)
        redir_obj = get_object_or_404(URLRedirect, short_link=short_link)
        redir_dict = model_to_dict(redir_obj)
        redir_dict.update(request.data)
        redir = URLRedirectSerializer(redir_obj, data=redir_dict)
        if redir.is_valid() is True:
            redir.save()
            return Response({"message": "Redirect successfully updated"})
        else:
            return Response({"message": url_redirect.errors}, 422)
