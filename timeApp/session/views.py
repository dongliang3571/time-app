from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponse
from django.http.response import JsonResponse
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
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
    template_name = 'session/user_create.html'


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
        qr_code_string = request.GET.get('qr_code_string', '')
        try:
            # try if the QRcode matches an existing user
            temp_user = TemporalUser.objects.get(qr_code_string=qr_code_string)
            current_session = UserSession.objects.filter(temporal_user=temp_user,
                                                         is_active=True)
            if current_session:
                current_session_single = current_session[0]
                current_session_single.is_active = False
                current_session_single.logout_time = timezone.now()
                current_session_single.save()
                return Response({
                    'user': temp_user.first_name + ' ' + temp_user.last_name,
                    'signed_in': current_session_single.login_time,
                    'signed_out': current_session_single.logout_time,
                    'total_minutes': current_session_single.calculate_total_minutes()
                })
            else:
                current_session_single = UserSession.objects.create(temporal_user=temp_user)
                return Response({
                    'user': temp_user.first_name + ' ' + temp_user.last_name,
                    'signed_in': str(current_session_single.login_time)
                })
        except ObjectDoesNotExist:
            print "QR code is not found in database"
            return Response({'Error': 'QR code is not found in database'})
        return Response({
            'Error': 'Server error, jumpped to end of function for no reason'
        })
