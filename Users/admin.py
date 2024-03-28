
# Register your models here.
from .models import Otp
from django.contrib import admin
from Users.models import User
from django.contrib.auth.admin import UserAdmin
from django.forms import Textarea
from django.db import models


class UserAdminConfig(UserAdmin):
    model = User
    search_fields = ('email', 'user_name', )
    list_filter = ("id", 'email', 'user_name',  'is_active', 'is_staff')
    ordering = ('-start_date',)
    list_display = ("id", 'u_id', 'email', 'user_name',
                    'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'user_name', )}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 20, 'cols': 60})},
    }

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'user_name',  'password1', 'password2', 'is_active', 'is_staff')}
         ),
    )


admin.site.register(User, UserAdminConfig)


class OtpAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_for', 'code', 'created_at')
    search_fields = ['created_for__email', 'code']


admin.site.register(Otp, OtpAdmin)
