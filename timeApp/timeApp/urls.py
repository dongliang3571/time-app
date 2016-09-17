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
from django.core.urlresolvers import reverse

from rest_framework_jwt.views import obtain_jwt_token
from registration.backends.simple.views import RegistrationView

from session.views import (TemporalUserCreateView, TemporalUserShowView,
                           SessionCreateAPIView, CurrentPunchedInEmployees,
                           EditEmployees, HistorySessionView)

class MyRegistrationView(RegistrationView):
    def get_success_url(self,request):
        return reverse('session-members')

urlpatterns = [
    ###########################################################################
    ################################# Admin Panel #############################
    ###########################################################################
    url(r'^admin/', include(admin.site.urls)),

    ###########################################################################
    ################################# API URL #################################
    ###########################################################################
    ## App: session
    # Session
    url(r'^api/session-create/?$', SessionCreateAPIView.as_view(), name='session-create'),

    ###########################################################################
    ############################ Web app URL ##################################
    ###########################################################################

    ## App: rest_framework
    # Rest framework Web Authentication urls
    url(r'^api/token-auth/?$', obtain_jwt_token),
    url(r'^api/auth/',
        include('rest_framework.urls',namespace='rest_framework')),

    ## App: dashboard
    # Index
    url(r'^$', 'index.views.index', name='index-index'),
    # About
    url(r'^about/$', 'index.views.about', name='index-about'),
    # Features
    url(r'^#features$', 'index.views.index', name='index-features'),
    # How it works
    url(r'^#how-it-works$', 'index.views.index', name='index-how-it-works'),
    # Contact
    url(r'^contact/$', 'index.views.contact', name='index-contact'),
    # FAQ
    url(r'^faq/$', 'index.views.faq', name='index-faq'),
    # Newsletter
    url(r'^newsletter/$', 'index.views.newsletter', name='index-newsletter'),

    # Account authentication and registration
    # url(r'^accounts/register/$', MyRegistrationView.as_view(),
    #     name='registration_register'),
    url(r'^accounts/', include('registration.backends.default.urls')),


    ################################ employees ################################
    # Add memeber
    url(r'^session/add-member/$',
        login_required(TemporalUserCreateView.as_view()),
        name='session-add-member'),
    # Member detail
    url(r'^session/members/(?P<pk>[-\w]+)/$',
        login_required(TemporalUserShowView.as_view()),
        name='session-memberdetail'),
    # Edit members profile
    url(r'^session/members/(?P<pk>[-\w]+)/edit$',
        login_required(EditEmployees.as_view()),
        name='session-member-edit'),
    # Delete members
    url(r'^session/members/(?P<pk>[-\w]+)/delete$',
        'session.views.DeleteEmployees',
        name='session-member-delete'),


    ############################## Sessions ###################################
    # Session current members signed in in dashboard
    url(r'^session/members/$',
        login_required(CurrentPunchedInEmployees.as_view()),
        name='session-members'),
    # Session manual clock out
    url(r'^session/clockout/$',
        'session.views.clockOut',
        name='session-manual-clockout'),
    # Session History
    url(r'^session/history/$',
        HistorySessionView.as_view(),
        name='session-history'),


    ############################# Department ##################################
    # Add departments
    url(r'^session/departments/create/$',
        'session.views.addDepartment',
        name='session-department-add'),
    # Delete departments
    url(r'^session/departments/(?P<pk>[-\w]+)/delete$',
        'session.views.deleteDepartment',
        name='session-department-delete'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
