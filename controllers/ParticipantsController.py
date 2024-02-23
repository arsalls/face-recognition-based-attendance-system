from datetime import datetime

from flask import request

from models.Attendances import Attendances
from models.Participants import Participants
from utilities.ai_helpers import add_face, take_attendance
from utilities.errors import unhandled, invalid
from utilities.helpers import success, fail


def add_participant():
    try:
        _json = request.json
        user_id = request.cookies.get('user')
        if _json and user_id:
            id = _json.get('id')
            name = _json.get('name')
            group = _json.get('group')

            participant_id = Participants.insert_participant(id=id, name=name, group=group, user_id=user_id)
            if isinstance(participant_id, Exception): raise participant_id

            if participant_id:
                face_img_paths = add_face(id=participant_id)
                if isinstance(face_img_paths, Exception): raise face_img_paths

                response = Participants.update_participant_face(id=participant_id, face_data=face_img_paths)
                if isinstance(response, Exception): raise response

                return success(data={"message":"Participant successfully added....."})
            else:
                return fail(data={"message":"user not added"}, status_code=200)
        return unhandled("invalid request")
    except Exception as e:
        return unhandled(e)
