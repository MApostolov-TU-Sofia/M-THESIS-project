from flask import Blueprint, session, request
from application.controller.data.process import data_upload_excel, anonymize_data
import os
import requests
from flask import Flask, render_template
from ms_identity_python.flask import Auth
from application import app, ms_auth

route_data_process_bp = Blueprint('route_data_process_bp', __name__)


def get_i_data(req):
    i_data = req.args.to_dict()
    if (req.method == 'POST'):
        i_data = req.get_json()
    return i_data


@route_data_process_bp.post('/upload_excel')
def route_data_process_upload_excel():
    return data_upload_excel()


@route_data_process_bp.post('/anonymize_data')
def route_anonymize_data():
    return anonymize_data(get_i_data(request))
