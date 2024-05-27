from datetime import datetime
from flask import render_template, jsonify
import os
import requests
from flask import Flask, redirect, url_for, render_template, session
from ms_identity_python.flask import Auth
from application import app
from application import ms_auth

__version__ = "0.9.0"  # The version of this sample, for troubleshooting purpose


def user_login_microsoft_index(context):
    session['user'] = context['user']
    return redirect('/')
    # return render_template(
    #     'user/login/microsoft.html',
    #     user=context['user'],
    #     edit_profile_url=ms_auth.get_edit_profile_url(),
    #     api_endpoint=os.getenv("ENDPOINT"),
    #     title=f"Flask Web App Sample v{__version__}",
    # )


def user_login_microsoft_call_api(context):
    session['user'] = context['user']
    api_result = requests.get(  # Use access token to call a web api
        os.getenv("ENDPOINT"),
        headers={'Authorization': 'Bearer ' + context['access_token']},
        timeout=30,
    ).json() if context.get('access_token') else "Did you forget to set the SCOPE environment variable?"
    return render_template('display.html', title="API Response", result=api_result)