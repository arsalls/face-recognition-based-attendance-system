import datetime

from flask import request

from models.Attendances import Attendances
from models.Participants import Participants
from utilities.ai_helpers import add_face, take_attendance
from utilities.errors import unhandled, invalid
from utilities.helpers import success, fail


def get_attendances():
    try:
        _json = request.json
        user_id = request.cookies.get('user')
        if _json and user_id:
            start_datetime = _json.get('startDateTime')
            end_datetime = _json.get('endDateTime')

            # '09/19/22'

            if start_datetime and end_datetime:
                if len(start_datetime) > 0 and len(end_datetime) > 0:
                    start_datetime = datetime.datetime.strptime(start_datetime, '%m/%d/%y')
                    end_datetime = datetime.datetime.strptime(end_datetime, '%m/%d/%y')
                    end_datetime = end_datetime + datetime.timedelta(days=1)

                    attendances = Attendances.get_attendances(user_id=user_id,
                                                                 start_datetime=start_datetime, end_datetime=end_datetime)
                    attendances = [{
                                    "name": attendance.get("name"),
                                    "group": attendance.get("group"),
                                    "mark_date": attendance.get("mark_datetime").strftime('%m/%d/%Y'),
                                    "mark_time": attendance.get("mark_datetime").strftime('%H:%M:%S')
                                    } for attendance in attendances]
                    if isinstance(attendances, Exception): raise attendances

                    return success(data=attendances)
            return success(data=[])
        return success(data=[])
    except Exception as e:
        return unhandled(e)


def mark_attendance():
    try:
        user_id = request.cookies.get('user')

        participant_id = take_attendance()
        if isinstance(participant_id, Exception): raise participant_id

        if participant_id:
            participant = Participants.get_participants(id=participant_id)
            if isinstance(participant, Exception): raise participant

            if not participant:
                return fail(data={"message":"Participant not found !"}, status_code=200)

            response = Attendances.mark_attendance(user_id=user_id, participant_id=participant_id)
            if isinstance(response, Exception): raise response

            return success(data={"message":f"Attendance marked for Participant: {participant.get('name')} Duration: {datetime.datetime.now().strftime('%m/%d/%Y, %H:%M:%S')}"})
        else:
            return fail(data={"message":"Face not detected. Please make camera adjustments or make sure Participant is registered !"}, status_code=200)
    except Exception as e:
        return unhandled(e)
