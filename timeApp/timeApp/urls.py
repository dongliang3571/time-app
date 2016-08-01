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
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required

from rest_framework_jwt.views import obtain_jwt_token

from session.views import (TemporalUserCreateView, TemporalUserShowView,
                           UserSessionCreateView, UserSessionShowView,
                           SessionCreateAPIView, CurrentSessionListView,
                           HistorySessionView)


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    ## App: session
    # User
    # url(r'^session/user/create/$', TemporalUserCreateView.as_view(),
    #     name='session-temporalusercreate'),
    # url(r'^session/user/(?P<pk>[-\w]+)/$', TemporalUserShowView.as_view(),
    #     name='session-temporalusershow'),

    # Session
    # url(r'^session/create/$', UserSessionCreateView.as_view(),
    #     name='session-usersessioncreate'),
    # url(r'^session/(?P<pk>[-\w]+)/$', UserSessionShowView.as_view(),
    #     name='session-usersessionshow'),

    # Rest framework Authentication urls
    url(r'^api/token-auth/?$', obtain_jwt_token),
    url(r'^api/auth/', include('rest_framework.urls',
                               namespace='rest_framework')),

    ## API URL
    ## App: session
    # Session
    url(r'^api/session-create/?$', SessionCreateAPIView.as_view()),

    ## Web app URL
    ## App: dashboard
    # Index
    url(r'^$', 'index.views.index', name='index-index'),

    # Login
    url(r'^login/$', 'index.views.organizationLogin', name='index-login'),
    # Logout
    url(r'^logout/$', 'index.views.organizationLogout', name='index-logout'),

    # Dashboard
    # url(r'^session/dashboard/$',
    #     'session.views.dashboard',
    #     name='session-dashboard'),

    # Add memeber
    url(r'^session/add-member/$',
        login_required(TemporalUserCreateView.as_view()),
        name='session-add-member'),
    # Member detail
    url(r'^session/members/(?P<pk>[-\w]+)/$',
        login_required(TemporalUserShowView.as_view()),
        name='session-memberdetail'),
    # List members in dashboard
    url(r'^session/members/$',
        login_required(CurrentSessionListView.as_view()),
        name='session-members'),

    # History
    url(r'^session/history/$',
        HistorySessionView.as_view(),
        name='session-history')

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
