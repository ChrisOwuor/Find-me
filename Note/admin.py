from django.contrib import admin
from .models import Note



class NoteAdmin(admin.ModelAdmin):
    list_display = ("id","user","body")
# Register your models here.
admin.site.register(Note, NoteAdmin)
