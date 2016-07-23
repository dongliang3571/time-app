"""timeApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from rest_framework_jwt.views import obtain_jwt_token

from session.views import (TemporalUserCreateView, TemporalUserShowView,
                           UserSessionCreateView, UserSessionShowView,
                           SessionCreateAPIView)
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    ## App: session
    # User
    url(r'^session/user/create/$', TemporalUserCreateView.as_view(),
        name='session-temporalusercreate'),
    url(r'^session/user/(?P<pk>[-\w]+)/$', TemporalUserShowView.as_view(),
        name='session-temporalusershow'),

    # Session
    url(r'^session/create/$', UserSessionCreateView.as_view(),
        name='session-usersessioncreate'),
    url(r'^session/(?P<pk>[-\w]+)/$', UserSessionShowView.as_view(),
        name='session-usersessionshow'),

    # Rest framework Authentication urls
    url(r'^api/token-auth/', obtain_jwt_token),
    url(r'^api/auth/', include('rest_framework.urls', namespace='rest_framework')),

    ## API URL
    ## App: session
    # Session
    url(r'^api/session-create/$', SessionCreateAPIView.as_view()),
]
