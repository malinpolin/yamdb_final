from django.conf import settings
from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    The class configures the admin panel interface
    for the user model.
    """

    list_display = ("pk", "username", "first_name",
                    "last_name", "email", "bio", "role")
    list_filter = ("username",)
    search_fields = ("username", "email", "bio")
    empty_value_display = settings.EMPTY_VALUE_DISPLAY
