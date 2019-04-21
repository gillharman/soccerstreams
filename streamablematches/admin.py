from django.contrib import admin
from .models import Links, StreamableMatch

def match(obj):
    return "%s" % obj.match.match

# Register your models here.
class LinksAdmin(admin.ModelAdmin):
    list_display = (match,)


def scanned_match(obj):
    return "%s" % obj.scanned_match.match

def match_name(obj):
    return "%s" % obj.match.display_name()


class StreamableMatchAdmin(admin.ModelAdmin):
    list_display = (scanned_match, match_name)


admin.site.register(Links, LinksAdmin)
admin.site.register(StreamableMatch, StreamableMatchAdmin)