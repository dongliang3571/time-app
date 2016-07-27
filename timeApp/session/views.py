from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponse
from django.http.response import JsonResponse
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import TemporalUser, UserSession
from .forms import TemporalUserCreateForm


class TemporalUserCreateView(CreateView):
    model = TemporalUser
    form_class = TemporalUserCreateForm
    template_name = 'session/session_add_member.html'

    def get_context_data(self, **kwargs):
        context = super(TemporalUserCreateView, self).get_context_data(**kwargs)
        context['total_members'] = TemporalUser.objects.get_total_member_for_organization(self.request.user)
        context['total_visitors'] = TemporalUser.objects.get_total_visitor_for_organization(self.request.user)
        return context


class TemporalUserShowView(DetailView):
    model = TemporalUser
    template_name = 'session/user_show.html'


class UserSessionCreateView(CreateView):
    model = UserSession
    template_name = 'session/session_create.html'
    fields = ['temporal_user']


class UserSessionShowView(DetailView):
    model = UserSession
    template_name = 'session/session_show.html'


class SessionCreateAPIView(APIView):
    # authentication_classes = (SessionAuthentication, JSONWebTokenAuthentication)
    # permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        # grab the QRcode string from post request body
        qr_code_string = request.POST.get('qr_code_string', '')
        try:
            # try if the QRcode matches an existing user
            temp_user = TemporalUser.objects.get(qr_code_string=qr_code_string)
        except ObjectDoesNotExist:
            print "QR code is not found in database"
            return Response({'Error': 'QR code is not found in database'})
        else:
            current_session = UserSession.objects.filter(temporal_user=temp_user,
                                                         is_active=True)
            if current_session:
                current_session_single = current_session[0]
                current_session_single.is_active = False
                current_session_single.logout_time = timezone.now()
                current_session_single.save()
                return Response({
                    'is_active': current_session_single.is_active,
                    'user': temp_user.first_name + ' ' + temp_user.last_name,
                    'team': temp_user.team,
                    'signed_in': current_session_single.proper_login_time_string(),
                    'signed_out': current_session_single.proper_logout_time_string(),
                    'total_minutes': current_session_single.calculate_total_minutes()
                })
            else:
                current_session_single = UserSession.objects.create(temporal_user=temp_user)
                return Response({
                    'is_active': current_session_single.is_active,
                    'user': temp_user.first_name + ' ' + temp_user.last_name,
                    'team': temp_user.team,
                    'signed_in': current_session_single.proper_login_time_string()
                })
        return Response({
            'Error': 'Server error, jumpped to end of function for no reason'
        })


@login_required
def dashboard(request):
    messages.error(request, 'dashboard')
    return render(request, 'session/session_dashboard.html')


@login_required
def addMember(request):
    messages.error(request, 'add member')
    return render(request, 'session/session_add_member.html')


@login_required
def history(request):
    messages.error(request, 'history')
    return render(request, 'session/session_history.html')
