from django.contrib import admin

# Register your models here.
from streamablematches.models.logs import RequestLog
admin.site.register(RequestLog)
