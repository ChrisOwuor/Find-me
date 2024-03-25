
# Create your models here.
from datetime import timezone
import random
import string
from django.db import models
from Api.models import MissingPerson

# Create your models here.


class Case(models.Model):
    case_number = models.CharField(
        max_length=50, default="", unique=True, editable=False)
    missing_person = models.ForeignKey(
        MissingPerson, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=20, choices=[(
        'open', 'Open'), ('closed', 'Closed')], default='open')
    notes = models.TextField(blank=True, default="")

    def generate_case_number(self):
        case_number = ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=8))

        if not Case.objects.filter(case_number=case_number).exists():
            return case_number

    def __str__(self):
        return f"Case {self.case_number}"

    def save(self, *args, **kwargs):
        if not self.case_number:
            self.case_number = self.generate_case_number()
        super().save(*args, **kwargs)
