from django.db import models

class Request(models.Model):
    description = models.CharField(max_length=450)
    color = models.CharField(max_length=7)