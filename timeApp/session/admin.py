from django.contrib import admin

from .models import TemporalUser, UserSession


admin.site.register(TemporalUser)
admin.site.register(UserSession)
