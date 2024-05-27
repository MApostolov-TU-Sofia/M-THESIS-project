from datetime import datetime
from flask import render_template, jsonify, session
from application import app
from application.controller.user import user_check_index


def home_index():
    lg_ms = '/user/login/microsoft'
    lg_google = '/user/login/google'
    lg_logout = '/user/logout'
    lg_user = session['user'] if session.get('user') else None
    lg_user = session['_logged_in_user'] if (lg_user is None and session.get('_logged_in_user')) else lg_user
    session['user'] = lg_user
    if (lg_user is not None):
        user_check_index()
    return render_template('home/index.html',
                           login_microsoft=lg_ms,
                           login_google=lg_google,
                           logout=lg_logout,
                           user=lg_user)


def page_not_found_index(error):
    return render_template('static/404.html'), 404