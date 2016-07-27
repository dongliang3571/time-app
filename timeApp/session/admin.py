from django.contrib import admin

from .models import Team, TemporalUser, UserSession


admin.site.register(Team)
admin.site.register(TemporalUser)
admin.site.register(UserSession)
