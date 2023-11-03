from django.contrib import admin
from .models import Stone, Activation


from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


class CustomUserAdmin(UserAdmin):
    list_display = ("id", "username", "email", "first_name", "last_name")


class StoneAdmin(admin.ModelAdmin):
    list_display = ("id", "stone_name")


class ActivationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "stone", "start_time", "end_time", "power_duration")


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

admin.site.register(Stone, StoneAdmin)
admin.site.register(Activation, ActivationAdmin)
