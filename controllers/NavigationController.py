from flask import render_template, make_response, session, redirect, url_for
from utilities.helpers import login_required


@login_required
def index():
    try:
        return render_template('index.html')
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