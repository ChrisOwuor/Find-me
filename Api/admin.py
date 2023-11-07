
# Register your models here.

from django.contrib import admin
from .models import MissingPerson, ReportedSeenPerson


class PersonAdmin(admin.ModelAdmin):
    list_display = ("id","trackCode", "created_by", "first_name",
                    "middle_name",
                    "nick_name",
                    "last_name",
                    "county",
                    "last_seen",
                    "eye_color",
                    "hair_color",
                    "age",
                    "location",
                    "description",
                    "image",
                    "gender",
                    "created_at",
                    "updated_at")


class FoundPersonAdmin(admin.ModelAdmin):
    list_display = ("id", "created_by", "first_name",
                    "middle_name",
                    "last_name",
                    "county",
                    "last_seen",
                    "eye_color",
                    "hair_color",
                    "age",
                    "location",
                    "description",
                    "image",
                    "gender", "created_at",
                    "updated_at")


# Register your models here.

admin.site.register(MissingPerson, PersonAdmin)
admin.site.register(ReportedSeenPerson, FoundPersonAdmin)
