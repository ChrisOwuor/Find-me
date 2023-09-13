

# Register your models here.

from django.contrib import admin
from .models import MissingPerson,ReportedSeenPerson


class PersonAdmin(admin.ModelAdmin):
    list_display = ("id","name","age", "location","description")


class FoundPersonAdmin(admin.ModelAdmin):
    list_display = ("id","name",  "age","description","matched")


# Register your models here.

admin.site.register(MissingPerson, PersonAdmin)
admin.site.register(ReportedSeenPerson, FoundPersonAdmin)

