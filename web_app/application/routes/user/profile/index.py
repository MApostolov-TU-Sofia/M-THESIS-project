from flask import Blueprint, redirect, session, request
from application.controller.user.profile.index import user_profile, user_change_password, user_register, user_login
from application import routes

route_user_profile_bp = Blueprint('route_profile_index', __name__)


@route_user_profile_bp.route('/register', methods=['GET', 'POST'])
def route_user_register():
    return user_register(request, routes.get_i_data(request))


@route_user_profile_bp.route('/login', methods=['GET', 'POST'])
def route_user_login():
    return user_login(request, routes.get_i_data(request))


@route_user_profile_bp.route('/profile', methods=['GET'])
def route_user_profile():
    return user_profile(request, routes.get_i_data(request))


@route_user_profile_bp.route('/change_password', methods=['POST'])
def route_user_change_password():
    return user_change_password(request, routes.get_i_data(request))


@route_user_profile_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')
