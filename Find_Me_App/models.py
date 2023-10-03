from django.db import models


# Create your models here.


class MissingPerson(models.Model):
    trackCode = models.CharField(max_length=10, unique=True, editable=False)
    name = models.CharField(max_length=80, null=False)
    age = models.IntegerField(null=False, default=23)
    location = models.CharField(max_length=100, default="Nairobi")
    description = models.CharField(max_length=1000, null=False, default="Tall")
    image = models.ImageField(upload_to='Find_Me_App/Mp_Imgs', default="")


class ReportedSeenPerson(models.Model):
    name = models.CharField(max_length=80, null=False)
    age = models.IntegerField(null=False, default=10)
    description = models.CharField(max_length=1000, null=False, default="Tall")
    matched = models.BooleanField(default=False)
    image = models.ImageField(upload_to='Find_Me_App/Fp_Imgs', default=" ")

