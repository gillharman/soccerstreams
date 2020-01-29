from django.contrib import admin

# Register your models here.
from streamablematches.models.logs import RequestLogs
admin.site.register(RequestLogs)
