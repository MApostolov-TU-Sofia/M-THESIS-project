from flask import Blueprint, session
from application.controller.user.login.microsoft import user_login_microsoft_index, user_login_microsoft_call_api
import os
import requests
from flask import Flask, render_template
from ms_identity_python.flask import Auth
from application import app, ms_auth

route_user_microsoft_bp = Blueprint('route_microsoft', __name__)

@route_user_microsoft_bp.route('/microsoft')
@ms_auth.login_required
def route_user_microsoft_login_index(context):
    return user_login_microsoft_index(context)


@app.route("/call_api")
@ms_auth.login_required(scopes=os.getenv("SCOPE", "").split())
def route_user_microsoft_call_downstream_api(*, context):
    return user_login_microsoft_call_api(context)


@app.route("/auth/callback")
@ms_auth.login_required(scopes=os.getenv("SCOPE", "").split())
def route_user_microsoft_redirect_uri(*, context):
    return user_login_microsoft_call_api(context)