from django.contrib import admin
from django.contrib.admin import TabularInline

from .models import Client, Appointment


class AppointmentInline(TabularInline):
    model = Appointment
    extra = 0
    max_num = 10

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    inlines = (AppointmentInline,)
    list_display = (
        "telegram_id",
        "name",
        "surname",
        "phone"
    )
    search_fields = (
        "name",
        "surname",
        "phone",
        "telegram_id"
    )


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "pet",
        "date",
        "owner"
    )
    search_fields = (
        "id",
        "pet",
        "date",
        "owner__name",
        "owner__phone",
        "owner__surname",
        "owner__telegram_id"
    )
