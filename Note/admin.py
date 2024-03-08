# your_app/admin.py

from django.contrib import admin
from .models import Case


class CaseAdmin(admin.ModelAdmin):
    list_display = ('case_number', 'missing_person', 'status', 'notes')
    search_fields = ('case_number', 'missing_person__first_name',
                     'missing_person__last_name')


admin.site.register(Case, CaseAdmin)
