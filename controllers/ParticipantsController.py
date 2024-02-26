import os
import threading
from flask import request

from models.Participants import Participants
from utilities.ai_helpers import add_face, take_attendance, train_model
from utilities.errors import unhandled, invalid
from utilities.helpers import success, fail, remove_folder_and_files


def action_participant():
    try:
        _json = request.json
        user_id = request.cookies.get('user')
        if _json and user_id:
            id = _json.get('id')
            name = _json.get('name')
            group = _json.get('group')
            action = _json.get('action')

            if action == "add":
                participant_id = Participants.insert_participant(id=id, name=name, group=group, user_id=user_id)
                if isinstance(participant_id, Exception): raise participant_id

                if participant_id:
                    face_img_paths = add_face(id=participant_id)
                    if isinstance(face_img_paths, Exception): raise face_img_paths

                    response = Participants.update_participant_face(id=participant_id, face_data=face_img_paths)
                    if isinstance(response, Exception): raise response

                    return success(data={"message":"Participant successfully added....."})
                else:
                    return fail(data={"message": "user not added"}, status_code=200)
            else:
                resposne = Participants.update_participant(id=id, name=name, group=group)
                if isinstance(resposne, Exception): raise resposne

                if resposne:
                    return success(data={"message":"Participant successfully updated....."})
                else:
                    return fail(data={"message": "user not updated"}, status_code=200)

        return unhandled("invalid request")
    except Exception as e:
        return unhandled(e)


def del_participant():
    try:
        _args = request.args
        participent_id = _args.get('participant')
        if participent_id:
            response = Participants.remove_participant(id=participent_id)
            if isinstance(response, Exception): raise response

            response = remove_folder_and_files(os.path.join(os.getenv("FACES_DIR"), participent_id))
            if isinstance(response, Exception): raise response

            threading.Thread(target=train_model, name="AI Modal Trainer").start()

            return success(data={"message":"Participant removed successfully....."})
        else:
            return fail(data={"message":"Participant not added"}, status_code=200)
    except Exception as e:
        return unhandled(e)


def get_participants():
    try:
        _args = request.args
        participent_id = _args.get('participant')
        response = Participants.get_participants(id=participent_id)
        if isinstance(response, Exception): raise response

        return success(data=response)
    except Exception as e:
        return unhandled(e)
