from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from app.internal.models.user import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'external_id', 'username')
