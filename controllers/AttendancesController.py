from datetime import datetime

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
            participant_id = _json.get('participant')

            attendances = Attendances.get_attendances(user_id=user_id, participant_id=participant_id,
                                                         start_datetime=start_datetime, end_datetime=end_datetime)
            if isinstance(attendances, Exception): raise attendances

            return success(data=attendances)
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

            return success(data={"message":f"Attendance marked for Participant: {participant.get('name')} Duration: {datetime.now().strftime('%m/%d/%Y, %H:%M:%S')}"})
        else:
            return fail(data={"message":"Face not detected. Please make camera adjustments or make sure Participant is registered !"}, status_code=200)
    except Exception as e:
        return unhandled(e)
