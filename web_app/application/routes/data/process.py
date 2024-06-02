from flask import Blueprint, session, request
from application.controller.data.process import data_upload_excel, anonymize_data
import os
import requests
from flask import Flask, render_template
from ms_identity_python.flask import Auth
from application import app, ms_auth
from application import routes

route_data_process_bp = Blueprint('route_data_process_bp', __name__)


@route_data_process_bp.post('/upload_excel')
def route_data_process_upload_excel():
    return data_upload_excel()


@route_data_process_bp.post('/anonymize_data')
def route_anonymize_data():
    return anonymize_data(routes.get_i_data(request))
