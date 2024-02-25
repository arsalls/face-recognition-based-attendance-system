from flask import render_template, make_response, session, redirect, url_for, request
from models.Participants import Participants
from utilities.helpers import login_required


@login_required
def index():
    try:
        user_id = request.cookies.get('user')
        participants = Participants.get_participants(user_id=user_id)
        if isinstance(participants, Exception): raise participants

        return render_template('index.html', participants=participants)
    except Exception as e:
        return str(e)

@login_required
def attendance():
    try:
        return render_template('attendance.html')
    except Exception as e:
        return str(e)


def sign_in():
    try:
        response = make_response(render_template('signin.html'))
        session.pop('user', None)
        response.set_cookie("user", '', expires=0)
        return response
    except Exception as e:
        return str(e)


def sign_up():
    try:
        session.pop('user', None)
        response = make_response(render_template('signup.html'))
        response.set_cookie("user", '', expires=0)
        return response
    except Exception as e:
        return str(e)


@login_required
def logout():
    try:
        return redirect(url_for('signin'))
    except Exception as e:
        return str(e)