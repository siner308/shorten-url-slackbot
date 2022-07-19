from django.contrib import admin


# Register your models here.
from apps.shortener.models import Shortener


class ShortenerAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'url')


admin.site.register(Shortener, ShortenerAdmin)