from django.utils import timezone
from django.db import models
from Users.models import NewUser


# Create your models here.


class MissingPerson(models.Model):
    created_by = models.ForeignKey(
        NewUser, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=50,default="")
    trackCode = models.CharField(max_length=10, unique=True, editable=False)
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50,default="")
    nick_name = models.CharField(max_length=50, blank=True)
    county = models.CharField(max_length=50,default="")
    last_seen = models.DateTimeField(default=timezone.now)
    eye_color = models.CharField(max_length=20,default="")
    hair_color = models.CharField(max_length=20,default="")
    age = models.PositiveIntegerField(default=20)
    location = models.CharField(max_length=100,default="")
    description = models.TextField(default="")
    image = models.ImageField(upload_to='static/missing_persons', null=True, blank=True)
    gender = models.CharField(max_length=10,default="")

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"




class ReportedSeenPerson(models.Model):
    created_by = models.ForeignKey(
        NewUser, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=50,default="")
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50,default="")
    county = models.CharField(max_length=50,default="")
    last_seen = models.DateTimeField(default=timezone.now)
    eye_color = models.CharField(max_length=20,default="")
    hair_color = models.CharField(max_length=20,default="")
    age = models.PositiveIntegerField(default=20)
    location = models.CharField(max_length=100,default="")
    description = models.TextField(default="")
    image = models.ImageField(upload_to='static/seen_persons', null=True, blank=True)
    gender = models.CharField(max_length=10,default="")

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

