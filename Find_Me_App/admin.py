

# Register your models here.

from django.contrib import admin
from .models import MissingPerson,ReportedSeenPerson


class PersonAdmin(admin.ModelAdmin):
    list_display = ("id","name", "code", "matched", "age", "reported_at", "description","location")


class FoundPersonAdmin(admin.ModelAdmin):
    list_display = ("name",  "matched", "age", "reported_at", "description","location")


# Register your models here.

admin.site.register(MissingPerson, PersonAdmin)
admin.site.register(ReportedSeenPerson, FoundPersonAdmin)

