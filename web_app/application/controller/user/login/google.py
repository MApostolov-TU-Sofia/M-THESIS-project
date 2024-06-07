from flask import Flask, redirect, url_for, session, request, render_template
from application import google_oauth


def user_login_google_index():
    redirect_uri = url_for('google_authorized', _external=True)
    return google_oauth.google.authorize_redirect(redirect_uri)


def user_login_google_authorized():
    token = google_oauth.google.authorize_access_token()
    user_info = token['userinfo']
    session['user'] = user_info
    return redirect('/')
