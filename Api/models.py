
from django.utils import timezone
from django.db import models
from Api.utils import generate_track_code
from Users.models import User


class MissingPerson(models.Model):
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=50, default="")
    trackCode = models.CharField(max_length=10, unique=True, editable=False)
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, default="")
    nick_name = models.CharField(max_length=50, blank=True)
    eye_color = models.CharField(max_length=20, default="")
    hair_color = models.CharField(max_length=20, default="")
    age = models.PositiveIntegerField(default=20)
    description = models.TextField(default="")
    image = models.ImageField(
        upload_to='static/missing_persons', null=True, blank=True)
    gender = models.CharField(max_length=10, default="")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def generate_track_code(self):
        return generate_track_code(200)

    def save(self, *args, **kwargs):
        self.trackCode = self.generate_track_code()
        super().save(*args, **kwargs)


class FoundPerson(models.Model):
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=50, default="")
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, default="")
    eye_color = models.CharField(max_length=20, default="")
    hair_color = models.CharField(max_length=20, default="")
    age = models.PositiveIntegerField(default=20)
    description = models.TextField(default="")
    image = models.ImageField(
        upload_to='static/seen_persons', null=True, blank=True)
    gender = models.CharField(max_length=10, default="")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class FoundPersonLocation(models.Model):
    county = models.CharField(max_length=50, default="", null=True, blank=True)
    name = models.CharField(max_length=50, default="", null=True, blank=True)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True)
    time_found = models.DateTimeField(default=timezone.now)
    found_person = models.OneToOneField(
        MissingPerson, on_delete=models.CASCADE)


class MissingPersonLocation(models.Model):
    county = models.CharField(max_length=50, default="", null=True, blank=True)
    name = models.CharField(max_length=50, default="", null=True, blank=True)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True)
    time_seen = models.DateTimeField(default=timezone.now)
    missing_person = models.OneToOneField(
        MissingPerson, on_delete=models.CASCADE)
