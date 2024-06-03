from flask import Blueprint, redirect, session, request
from application.controller.project.index import project_modify, project_delete
from application import routes

route_project_bp = Blueprint('route_project_index', __name__)


@route_project_bp.route('/modify', methods=['POST'])
def route_project_modify():
    return project_modify(request, routes.get_i_data(request))


@route_project_bp.route('/delete', methods=['POST'])
def route_project_delete():
    return project_delete(request, routes.get_i_data(request))