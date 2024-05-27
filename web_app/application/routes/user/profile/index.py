from flask import Blueprint, redirect, session
from application.controller.user.profile.index import user_login_profile_index

route_user_profile_bp = Blueprint('route_profile_index', __name__)


@route_user_profile_bp.route('/profile')
def route_user_profile_index():
    return user_login_profile_index()


@route_user_profile_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')