def deserializerSession(sessions):
    data_list = []
    for session in sessions:
        data = {}
        data['date'] = session.proper_login_date_string
        data['name'] = session.temporal_user.__unicode__()
        data['team'] = str(session.temporal_user.team)
        data['sign_in'] = session.proper_login_time_only_string()
        data['sign_out'] = session.proper_logout_time_only_string()
        data['total_hours'] = session.total_time_in_hours()
        data_list.append(data)
    return data_list
