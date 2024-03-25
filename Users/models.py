from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
import random
from django.conf import settings
import uuid



class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, user_name,  password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, user_name,  password, **other_fields)

    def create_user(self, email, user_name,  password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name,
                          **other_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    user_name = models.CharField(max_length=150)
    start_date = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    u_id = models.UUIDField(editable=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name']

    def __str__(self):
        return self.user_name

    def save(self, *args, **kwargs):
        if not self.u_id:
            unique_uuid = uuid.uuid4()
            while User.objects.filter(u_id=unique_uuid).exists():
                unique_uuid = uuid.uuid4()
            self.u_id = unique_uuid
        super().save(*args, **kwargs)


class Otp(models.Model):
    created_for = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True)
    code = models.CharField(max_length=7)
    created_at = models.DateTimeField(default=timezone.now)

    def is_valid(self):
        """get 10 mins otp"""
        otp_time_sec = float(settings.OTP_EXPIRE_TIME * 60)
        current_time = timezone.now()
        time_diff = current_time - self.created_at

        return time_diff.total_seconds() <= otp_time_sec

    @classmethod
    def get_code(cls):
        random_number = random.randint(1000, 9999)
        return random_number
