
# Register your models here.

from django.contrib.auth.models import Group
from django.contrib import admin
from .models import MissingPerson, FoundPerson


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
                    "image",
                    "gender", "created_at",
                    "updated_at")




admin.site.register(MissingPerson, PersonAdmin)
admin.site.register(FoundPerson, FoundPersonAdmin)

# Deregister the Group model from the admin site
admin.site.unregister(Group)
