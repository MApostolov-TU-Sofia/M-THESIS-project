from flask import Blueprint
from application.controller.user.login.google import user_login_google_index, user_login_google_authorized
from application import app

route_user_google_bp = Blueprint('route_google', __name__)


@route_user_google_bp.route('/google')
def route_user_google_login_index():
    return user_login_google_index()


@app.route('/auth/callback/google')
def google_authorized():
    return user_login_google_authorized()