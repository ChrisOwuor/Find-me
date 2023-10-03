

# Register your models here.

from django.contrib import admin
from .models import MissingPerson,ReportedSeenPerson


class PersonAdmin(admin.ModelAdmin):
    list_display = ("id","trackCode","name","age", "location","description","image")


class FoundPersonAdmin(admin.ModelAdmin):
    list_display = ("id","name",  "age","description","matched","image")


# Register your models here.

admin.site.register(MissingPerson, PersonAdmin)
admin.site.register(ReportedSeenPerson, FoundPersonAdmin)

