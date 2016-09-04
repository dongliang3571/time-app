from datetime import datetime, timedelta

from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponse, get_object_or_404
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

from .models import Department, TemporalUser, UserSession
from .forms import TemporalUserCreateForm, DateFilterForm
from .utils import (deserializerSession, calculate_total_salary_for_sessions,
                    get_searched_sessions)


##########################APIs####################################
class SessionCreateAPIView(APIView):
    """
    Method: POST
    Description: iPad will use this api to clock in or clock out
    """
    # authentication_classes = (SessionAuthentication, JSONWebTokenAuthentication)
    # permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        # grab the QRcode string from post request body
        qr_code_string = request.GET.get('qr_code_string', '')
        time_string = request.GET.get('time_now', '')
        format = '%Y-%m-%d %H:%M:%S'
        try:
            time_now = datetime.strptime(time_string, format)
        except ValueError:
            print 'Date Time format is not correct'
            return Response({'Error': 'Date Time format is not correct'})
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
                current_session_single.logout_time = time_now
                current_session_single.calculate_total_minutes()
                current_session_single.calculate_total_salary()
                current_session_single.save()
                try:
                    return Response({
                        'is_active': current_session_single.is_active,
                        'user': temp_user.__unicode__(),
                        'department': str(temp_user.department),
                        'signed_in': (current_session_single
                                      .proper_login_time_string()),
                        'signed_out': (current_session_single
                                       .proper_logout_time_string()),
                        'total_minutes': current_session_single.total_minutes,
                        'total_salary': current_session_single.total_salary
                    })
                except:
                    return Response({
                        'Error': 'Error happened when return the results'
                    })
            else:
                current_session_single = (
                    UserSession
                    .objects
                    .create(temporal_user=temp_user)
                )
                current_session_single.login_time = time_now
                current_session_single.save()
                try:
                    return Response({
                        'is_active': current_session_single.is_active,
                        'user': temp_user.first_name + ' ' + temp_user.last_name,
                        'department': str(temp_user.department),
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

    def form_invalid(self, form):
        print "form is invalid"
        return super(TemporalUserCreateView, self).form_invalid(form)


class TemporalUserShowView(DetailView):
    """
    Method: GET
    Description: Show the detail of a member
    """
    model = TemporalUser
    template_name = 'session/session_member_detail.html'


################################Sessions################################

class CurrentPunchedInEmployees(View):
    def get(self, request):
        template_name = 'session/session_dashboard.html'
        context = {}
        currentSessions = (
            UserSession
            .objects
            .get_active_sessions_for_organization(self.request.user)
        )
        AllEmp = TemporalUser.objects.all()
        context['currentSessions'] = currentSessions
        context['allEmp'] = AllEmp

        return render(request, template_name, context)


class EditEmployees(View):
    def get(self, request, pk):
        template_name = 'session/session_member_edit.html'
        context = {}
        employee = get_object_or_404(TemporalUser, pk=pk)
        editForm = TemporalUserCreateForm(instance=employee)
        context['employee'] = employee
        context['editForm'] = editForm
        return render(request, template_name, context)

    def post(self, request, pk):
        employee = get_object_or_404(TemporalUser, pk=pk)
        editForm = TemporalUserCreateForm(request.POST, instance=employee)
        context = {}
        if editForm.is_valid():
            template_name = 'session/session_success.html'
            editForm.save()
            context['action'] = 'edited'
            return render(request, template_name, context)
        context['editForm'] = editForm
        template_name = 'session/session_member_edit.html'
        return render(request, template_name, context)


@login_required
def DeleteEmployees(request, pk):
    employee = get_object_or_404(TemporalUser, pk=pk)
    employee.delete()
    template_name = 'session/session_success.html'
    context = {'action': 'deleted'}
    return render(request, template_name, context)


class HistorySessionView(View):
    def get(self, request):
        format = '%m/%d/%Y'
        context = {}
        form = DateFilterForm(request.GET)
        context['form'] = form
        end_date = request.GET.get('end_date', None)
        start_date = request.GET.get('start_date', None)
        keyword = request.GET.get('keyword', None)

        # when search by all three fields
        if end_date and start_date and keyword:
            try:
                employees = TemporalUser.objects.filter(full_name__icontains=keyword)
            except ObjectDoesNotExist:
                context['error'] = "No employee found"
                return render(request, 'session/session_history.html', context)
            else:
                # calls utility function to get session and salary
                result_data, salary_data = get_searched_sessions(start_date=start_date,
                                                                 end_date=end_date,
                                                                 employees=employees)
                if result_data and salary_data:
                    context['employees_sessions'] = result_data
                    context['employees_salary'] = salary_data
                else:
                    context['error'] = "No employee found"
            return render(request, 'session/session_history.html', context)
        # when search by both start date and keyword
        elif start_date and keyword:
            try:
                employees = TemporalUser.objects.filter(full_name__icontains=keyword)
            except ObjectDoesNotExist:
                context['error'] = "No employee found"
                return render(request, 'session/session_history.html', context)
            else:
                # calls utility function to get session and salary
                result_data, salary_data = get_searched_sessions(start_date=start_date,
                                                                 employees=employees)
                if result_data and salary_data:
                    context['employees_sessions'] = result_data
                    context['employees_salary'] = salary_data
                else:
                    context['error'] = "No employee found"
            return render(request, 'session/session_history.html', context)
        # when only serach by start date and end date
        elif start_date and end_date:
            # calls utility function to get session and salary
            result_data, salary_data = get_searched_sessions(start_date=start_date,
                                                             end_date=end_date)
            if result_data and salary_data:
                context['employees_sessions'] = result_data
                context['employees_salary'] = salary_data
            else:
                context['error'] = "No employee found"
            return render(request, 'session/session_history.html', context)
        # when only search by start date
        elif start_date:
            # calls utility function to get session and salary
            result_data, salary_data = get_searched_sessions(start_date=start_date)
            if result_data and salary_data:
                context['employees_sessions'] = result_data
                context['employees_salary'] = salary_data
            else:
                context['error'] = "No employee found"
            return render(request, 'session/session_history.html', context)
        # when only search by keyword
        elif keyword:
            try:
                employees = TemporalUser.objects.filter(full_name__icontains=keyword)
            except ObjectDoesNotExist:
                context['error'] = "No employee found"
                return render(request, 'session/session_history.html', context)
            else:
                # get all history session for the employee
                # calls utility function to get session and salary
                result_data, salary_data = get_searched_sessions(employees=employees)
                if result_data and salary_data:
                    context['employees_sessions'] = result_data
                    context['employees_salary'] = salary_data
                else:
                    context['error'] = "No employee found"
            return render(request, 'session/session_history.html', context)
        else:
            context['error'] = 'Use search functionality'
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
