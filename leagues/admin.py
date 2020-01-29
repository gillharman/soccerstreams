from django.contrib import admin
from streamablematches.models.competitions import LeagueCopy


# Register your models here.
class LeagueAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "tracked")


admin.site.register(LeagueCopy, LeagueAdmin)
