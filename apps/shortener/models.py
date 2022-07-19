from django.db import models


class Shortener(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.CharField(max_length=2048, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, auto_created=True)

    objects = models.Manager()  # Default Manager
