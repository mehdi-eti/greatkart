from asyncore import read
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Account
# Register your models here.


class AccountAdmin(UserAdmin):
    list_display = ('email', "first_name", "last_name",
                    "username", 'last_login', 'date_joined', 'is_active')
    list_display_links = ('email', 'first_name', 'last_name')
    read_only_fields=('last_login', 'date_jaoined')
    ordering=('-date_joined', )
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Account, AccountAdmin)
