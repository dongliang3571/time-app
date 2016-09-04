from django.contrib import admin

from .models import Department, TemporalUser, UserSession


admin.site.register(Department)
admin.site.register(TemporalUser)
admin.site.register(UserSession)
