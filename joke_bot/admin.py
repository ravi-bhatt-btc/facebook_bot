from django.contrib import admin
from .models import *

# Register your models here.
class UsersAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone']
    readonly_fields=('sender_id',)

admin.site.register(Users, UsersAdmin)