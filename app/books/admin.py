from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

from .models import CustomUser, Book


@admin.register(CustomUser)
class UserAdmin(DefaultUserAdmin):
    pass


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    fields = ("title", "author")
    list_display = ("title", "author", "created_date", "updated_date")
    readonly_fields = ("created_date", "updated_date")