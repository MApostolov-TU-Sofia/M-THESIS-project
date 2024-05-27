from flask_sqlalchemy import SQLAlchemy
from flask import Flask, Blueprint
import os
import requests
from flask import Flask, render_template
from ms_identity_python.flask import Auth
from authlib.integrations.flask_client import OAuth
from config import Config

DATABASE_URL = 'mysql+mysqlconnector://tu_user:tu_sofia_psw@localhost:3306/tu_sofia_anonymize_app'

app = Flask(__name__, template_folder='views', static_folder='public')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_object(Config)
db = SQLAlchemy(app)

ms_auth = Auth(
    app,
    authority=Config.MS_AUTHORITY,
    client_id=Config.MS_CLIENT_ID,
    client_credential=Config.MS_CLIENT_SECRET,
    redirect_uri=Config.MS_REDIRECT_PATH,
    oidc_authority=Config.MS_OIDC_AUTHORITY,
    b2c_tenant_name=Config.MS_B2C_TENANT_NAME,
    b2c_signup_signin_user_flow=Config.MS_SIGNUPSIGNIN_USER_FLOW,
    b2c_edit_profile_user_flow=Config.MS_EDITPROFILE_USER_FLOW,
    b2c_reset_password_user_flow=Config.MS_RESETPASSWORD_USER_FLOW,
)

google_oauth = OAuth(app)
google_auth = google_oauth.register(
    name='google',
    client_id=Config.GOOGLE_CLIENT_ID,
    client_secret=Config.GOOGLE_CLIENT_SECRET,
    server_metadata_url=Config.GOOGLE_DISCOVERY_URL,
    client_kwargs={'scope': 'openid profile email'}
)

from application import model

import application.controller.home
# import app09.application.controller.role
# import app09.application.controller.user
# import app09.application.controller.bank
# import app09.application.controller.bank_account
# import app09.application.controller.credit_card
# import app09.application.controller.transaction

# import app09.application.routes.role
# import app09.application.routes.user
# import app09.application.routes.bank
# import app09.application.routes.bank_account
# import app09.application.routes.credit_card
# import app09.application.routes.transaction


from .routes import home, user

with app.app_context():
    db.create_all()