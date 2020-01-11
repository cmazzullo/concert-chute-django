from django.db import models


class Concert(models.Model):
    eventful_id = models.CharField(max_length=100, primary_key=True)
    title = models.TextField(null=True)
    description = models.TextField(null=True)
    url = models.URLField(max_length=500, null=True)
    start_time = models.DateTimeField()
    recur_string = models.CharField(max_length=500, null=True)

    venue = models.ForeignKey('Venue', on_delete=models.CASCADE)

    class Meta:
        ordering = ['start_time']


class Venue(models.Model):
    eventful_id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=1000, null=True)
    url = models.URLField(max_length=1000, null=True)
    city = models.CharField(max_length=400, null=True)
    country = models.CharField(max_length=400, null=True)
    region = models.CharField(max_length=400, null=True)
    address = models.TextField(null=True)
