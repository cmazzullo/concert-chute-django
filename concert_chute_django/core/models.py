from django.db import models


class Concert(models.Model):
    venue = models.CharField(max_length=1000)
    title = models.CharField(max_length=1000)
    start_time = models.DateTimeField()
