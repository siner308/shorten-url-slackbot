from django.shortcuts import redirect
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response


# Create your views here.
from apps.shortener.models import Shortener


class ShortenerViewSet(ViewSet):
    def retrieve(self, request, pk):
        shortener = Shortener.objects.filter(pk=pk).last()
        if not shortener:
            return Response(status=404)
        return redirect(shortener.url)
