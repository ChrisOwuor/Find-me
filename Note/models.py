
# Create your models here.
from django.db import models
from Users.models import User
# Create your models here.


class Note(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    body = models.TextField()


    def __str__(self):
        return self.body
    