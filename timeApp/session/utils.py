from datetime import datetime, timedelta
from itertools import chain

from .models import UserSession

def deserializerSession(sessions):
    data_list = []
    for session in sessions:
        data = {}
        data['date'] = session.proper_login_date_string
        data['name'] = session.temporal_user.__unicode__()
        data['department'] = str(session.temporal_user.department)
        data['sign_in'] = session.proper_login_time_only_string()
        data['sign_out'] = session.proper_logout_time_only_string()
        data['total_hours'] = session.total_time_in_hours()
        data['total_salary'] = session.total_salary_string()
        data_list.append(data)
    return data_list


def calculate_total_salary_for_sessions(sessions):
    total_salary = 0
    for session in sessions:
        total_salary += session['total_salary']
    return {
        'name': sessions[0]['name'],
        'salary': total_salary
    }


def process_sessions(sessions):
    if employee_sessions:
        # Collect all sessions
        data_list = deserializerSession(employee_sessions)
        result_data += data_list
        # Collect all salary for each searched employee
        salary_data.append(calculate_total_salary_for_sessions(data_list))
    else:
        pass

def get_searched_sessions(start_date=None, end_date=None, employees=None):
    format = '%m/%d/%Y'
    result_data = []
    salary_data = []

    # # when search by all three fields
    if start_date is not None and end_date is not None and employees is not None:
        date1 = datetime.strptime(start_date, format)
        # Add timedelta 1 day because login_time__range does not include end_date.
        date2 = datetime.strptime(end_date, format) + timedelta(days=1)
        for employee in employees:
            employee_sessions = (
                UserSession
                .objects
                .get_inactive_sessions_for_employee_start_date_end_date(
                    employee,
                    date1,
                    date2
                )
            )
            if employee_sessions:
                # Collect all sessions
                data_list = deserializerSession(employee_sessions)
                result_data += data_list
                # Collect all salary for each searched employee
                salary_data.append(calculate_total_salary_for_sessions(data_list))
            else:
                pass
    # when search by both start date and keyword
    elif start_date is not None and employees is not None:
        date1 = datetime.strptime(start_date, format)
        for employee in employees:
            employee_sessions = (
                UserSession
                .objects
                .get_inactive_sessions_for_employee_start_date(employee, date1)
            )
            if employee_sessions:
                # Collect all sessions
                data_list = deserializerSession(employee_sessions)
                result_data += data_list
                # Collect all salary for each searched employee
                salary_data.append(calculate_total_salary_for_sessions(data_list))
            else:
                pass
    # when only serach by start date and end date
    elif start_date is not None and end_date is not None:
        date1 = datetime.strptime(start_date, format)
        # Add timedelta 1 day because login_time__range does not include end_date.
        date2 = datetime.strptime(end_date, format) + timedelta(days=1)
        employee_sessions = (
            UserSession
            .objects
            .get_inactive_sessions_for_start_date_end_date(
                date1,
                date2
            )
        )
        if employee_sessions:
            separate_emp_dict = {}
            session_list = []
            # separate session into different element in dict by employees' names
            for session in employee_sessions:
                separate_emp_dict[session.get_name()] = separate_emp_dict.get(session.get_name(), []) + [session]
            for emp in separate_emp_dict:
                # Collect all sessions
                data_list = deserializerSession(separate_emp_dict[emp])
                result_data += data_list
                # Collect all salary for each searched employee
                salary_data.append(calculate_total_salary_for_sessions(data_list))
        else:
            pass
    # when only search by start date
    elif start_date is not None:
        date1 = datetime.strptime(start_date, format)
        employee_sessions = (
            UserSession
            .objects
            .get_inactive_sessions_for_start_date(date1)
        )
        if employee_sessions:
            separate_emp_dict = {}
            session_list = []
            # separate session into different element in dict by employees' names
            for session in employee_sessions:
                separate_emp_dict[session.get_name()] = separate_emp_dict.get(session.get_name(), []) + [session]
            for emp in separate_emp_dict:
                # Collect all sessions
                data_list = deserializerSession(separate_emp_dict[emp])
                result_data += data_list
                # Collect all salary for each searched employee
                salary_data.append(calculate_total_salary_for_sessions(data_list))
        else:
            pass
    # when only search by keyword
    elif employees is not None:
        for employee in employees:
            employee_sessions = (
                UserSession
                .objects
                .get_inactive_sessions_for_employee(employee)
            )
            if employee_sessions:
                # Collect all sessions
                data_list = deserializerSession(employee_sessions)
                result_data += data_list
                # Collect all salary for each searched employee
                salary_data.append(calculate_total_salary_for_sessions(data_list))
            else:
                pass

    return result_data, salary_data
