from flask import Blueprint, session
from application.controller.data.process import data_upload_excel
import os
import requests
from flask import Flask, render_template
from ms_identity_python.flask import Auth
from application import app, ms_auth

route_data_process_bp = Blueprint('route_data_process_bp', __name__)


@route_data_process_bp.post('/upload_excel')
def route_data_process_upload_excel():
    return data_upload_excel()
