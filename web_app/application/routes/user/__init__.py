from flask import Blueprint

# Importing sub-route blueprints
from .login.microsoft import route_user_microsoft_bp
from .login.google import route_user_google_bp
from .profile.index import route_user_profile_bp
from app import app


app.register_blueprint(route_user_microsoft_bp, url_prefix='/user/login')
app.register_blueprint(route_user_google_bp, url_prefix='/user/login')
app.register_blueprint(route_user_profile_bp, url_prefix='/user')