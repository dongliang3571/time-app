from datetime import datetime
from datetime import timedelta

from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponse
from django.http.response import JsonResponse
from django.views.generic import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import Team, TemporalUser, UserSession
from .forms import TemporalUserCreateForm, DateFilterForm
from .utils import deserializerSession


##########################APIs####################################
class SessionCreateAPIView(APIView):
    """
    Method: POST
    Description: iPad will use this api to clock in or clock out
    """
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
                try:
                    return Response({
                        'is_active': current_session_single.is_active,
                        'user': temp_user.__unicode__(),
                        'team': str(temp_user.team),
                        'signed_in': (current_session_single
                                      .proper_login_time_string()),
                        'signed_out': (current_session_single
                                       .proper_logout_time_string()),
                        'total_minutes': (current_session_single
                                          .calculate_total_minutes())
                    })
                except:
                    return Response({
                        'Error': 'Error happened when return the results'
                    })
            else:
                try:
                    current_session_single = (
                        UserSession
                        .objects
                        .create(temporal_user=temp_user)
                        )
                    return Response({
                        'is_active': current_session_single.is_active,
                        'user': temp_user.first_name + ' ' + temp_user.last_name,
                        'team': str(temp_user.team),
                        'signed_in': (current_session_single
                                      .proper_login_time_string())
                    })
                except:
                    return Response({
                        'Error': 'Error happened when return the results'
                    })
        return Response({
            'Error': 'Server error, jumpped to end of function for no reason'
        })


##############################Members####################################
class TemporalUserCreateView(CreateView):
    """
    Method: GET, POST
    Description: Show create form when making GET request, actually create the
    member when making POST request
    """
    model = TemporalUser
    form_class = TemporalUserCreateForm
    template_name = 'session/session_add_member.html'

    def form_valid(self, form):
        form.instance.organization = self.request.user
        return super(TemporalUserCreateView, self).form_valid(form)

    def form_invalid(self):
        print "form is invalid"
        return super(TemporalUserCreateView, self).form_invalid()

    # def get_context_data(self, **kwargs):
    #     context = super(TemporalUserCreateView, self).get_context_data(**kwargs)
    #     context['total_members_session'] = (
    #         UserSession
    #         .objects
    #         .get_active_members_sessions_for_organization(self.request.user)
    #         .count()
    #         )
    #     context['total_visitors_session'] = (
    #         UserSession
    #         .objects
    #         .get_active_visitors_sessions_for_organization(self.request.user)
    #         .count()
    #         )
    #     return context


class TemporalUserShowView(DetailView):
    """
    Method: GET
    Description: Show the detail of a member
    """
    model = TemporalUser
    template_name = 'session/session_member_detail.html'


################################Sessions################################
class CurrentSessionListView(ListView):
    model = UserSession
    context_object_name = 'sessions'
    template_name = 'session/session_dashboard.html'

    def get_queryset(self):
        return (UserSession
                .objects
                .get_active_sessions_for_organization(self.request.user))

    # def get_context_data(self, **kwargs):
    #     context = super(CurrentSessionListView, self).get_context_data(**kwargs)
    #     context['total_members_session'] = (
    #         UserSession
    #         .objects
    #         .get_active_members_sessions_for_organization(self.request.user)
    #         .count()
    #         )
    #     context['total_visitors_session'] = (
    #         UserSession
    #         .objects
    #         .get_active_visitors_sessions_for_organization(self.request.user)
    #         .count()
    #         )
    #     return context


class HistorySessionView(View):
    def get(self, request):
        context = {}
        form = DateFilterForm(request.GET)
        context['form'] = form
        end_date = request.GET.get('end_date', '')
        start_date = request.GET.get('start_date', '')
        keyword = request.GET.get('keyword', '')

        # when search by all three fields
        if end_date and start_date and keyword:
            print "all have"
            try:
                team = Team.objects.get(name__contains=keyword)
            except ObjectDoesNotExist:
                context['error'] = "No team found"
                return render(request, 'session/session_history.html', context)
            else:
                format = '%m/%d/%Y'
                date1 = datetime.strptime(start_date, format)
                # Add timedelta 1 day because login_time__range does not include
                # end_date.
                date2 = datetime.strptime(end_date, format) + timedelta(days=1)
                team_session = (
                    UserSession
                    .objects
                    .get_inactive_sessions_for_team_start_date_end_date(
                        team,
                        date1,
                        date2
                        )
                    )
                if team_session:
                    data_list = deserializerSession(team_session)
                    context['team_session'] = data_list
                else:
                    context['error'] = "No team found"
            return render(request, 'session/session_history.html', context)
        # when search by both start date and keyword
        elif start_date and keyword:
            print "have 2"
            try:
                team = Team.objects.get(name__contains=keyword)
            except ObjectDoesNotExist:
                context['error'] = "No team found"
                return render(request, 'session/session_history.html', context)
            else:
                format = '%m/%d/%Y'
                date = datetime.strptime(start_date, format)
                team_session = (
                    UserSession
                    .objects
                    .get_inactive_sessions_for_team_start_date(team, date)
                    )
                if team_session:
                    data_list = deserializerSession(team_session)
                    context['team_session'] = data_list
                else:
                    context['error'] = "No team found"
            return render(request, 'session/session_history.html', context)
        # when only search by start date
        elif start_date:
            print "have start_date only"
            format = '%m/%d/%Y'
            date = datetime.strptime(start_date, format)
            team_session = (
                UserSession
                .objects
                .get_inactive_sessions_for_start_date(date)
                )
            if team_session:
                data_list = deserializerSession(team_session)
                context['team_session'] = data_list
            else:
                context['error'] = "No team found"
            return render(request, 'session/session_history.html', context)
        # when only search by keyword
        elif keyword:
            print "have keyword only"
            try:
                team = Team.objects.get(name__contains=keyword)
            except ObjectDoesNotExist:
                context['error'] = "No team found"
                return render(request, 'session/session_history.html', context)
            else:
                # get all history session for the team
                team_session = (
                    UserSession
                    .objects
                    .get_inactive_sessions_for_team(team)
                    )
                if team_session:
                    data_list = deserializerSession(team_session)
                    context['team_session'] = data_list
                else:
                    context['error'] = "No team found"
            return render(request, 'session/session_history.html', context)
        else:
            context['error'] = 'No team found'
            return render(request, 'session/session_history.html', context)



@login_required
def addMember(request):
    messages.error(request, 'add member')
    return render(request, 'session/session_add_member.html')


# @login_required
# def history(request):
#     messages.error(request, 'history')
#     return render(request, 'session/session_history.html')


class UserSessionCreateView(CreateView):
    model = UserSession
    template_name = 'session/session_create.html'
    fields = ['temporal_user']


class UserSessionShowView(DetailView):
    model = UserSession
    template_name = 'session/session_show.html'
