
# Create your models here.
from django.db import models
from Users.models import NewUser
# Create your models here.


class Note(models.Model):
    user = models.ForeignKey(NewUser,on_delete=models.CASCADE, null=True)
    body = models.TextField()


    def __str__(self):
        return self.body
    