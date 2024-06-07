import os
import requests
from flask import Flask, redirect, url_for, render_template, session

__version__ = "0.9.0"


def user_login_microsoft_index(context):
    session['user'] = context['user']
    return redirect('/')


def user_login_microsoft_call_api(context):
    session['user'] = context['user']
    api_result = requests.get(  # Use access token to call a web api
        os.getenv("ENDPOINT"),
        headers={'Authorization': 'Bearer ' + context['access_token']},
        timeout=30,
    ).json() if context.get('access_token') else "Did you forget to set the SCOPE environment variable?"
    return render_template('display.html', title="API Response", result=api_result)
