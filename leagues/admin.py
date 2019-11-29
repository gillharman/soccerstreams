from django.contrib import admin
from .models import League

# Register your models here.
class LeagueAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "tracked")

admin.site.register(League, LeagueAdmin)