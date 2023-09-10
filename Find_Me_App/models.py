from django.db import models
# Create your models here.

from . import sandbox
gen_code = sandbox.gen_code()


class MissingPerson(models.Model):
    name = models.CharField(max_length=80, null=False)
    code = models.CharField(default=gen_code,max_length=20)
    matched = models.BooleanField(default=False)
    age = models.IntegerField(null=False)
    location = models.CharField(max_length=100,default="Nairobi")
    reported_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=500)


class ReportedSeenPerson(models.Model):
    name = models.CharField(max_length=80, null=False)
    matched = models.BooleanField(default=False)
    age = models.IntegerField(null=True)
    location = models.CharField(max_length=100,default="Nairobi")
    reported_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=500)
