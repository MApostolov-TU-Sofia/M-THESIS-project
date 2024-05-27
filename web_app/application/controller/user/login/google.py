from datetime import datetime
from flask import render_template, jsonify
import os
import requests
from flask import Flask, render_template
from ms_identity_python.flask import Auth
from flask import Flask, redirect, url_for, session, request, render_template
from application import google_oauth
from application.model import user as user_db


def user_login_google_index():
    redirect_uri = url_for('google_authorized', _external=True)
    return google_oauth.google.authorize_redirect(redirect_uri)


def user_login_google_authorized():
    token = google_oauth.google.authorize_access_token()
    user_info = token['userinfo']
    session['user'] = user_info
    return redirect('/')

