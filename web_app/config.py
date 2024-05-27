import os

class Config:
    SECRET_KEY = os.urandom(24)
    SESSION_TYPE = 'filesystem'

    # Microsoft OAuth settings
    MS_CLIENT_ID = ''
    MS_CLIENT_SECRET = ''
    MS_REDIRECT_PATH = ''
    MS_AUTHORITY = 'https://login.microsoftonline.com/common'
    MS_SCOPE = ['User.Read']
    MS_B2C_TENANT_NAME = ''
    MS_OIDC_AUTHORITY = ''
    MS_SIGNUPSIGNIN_USER_FLOW = '' # B2C_1_signinpolicy
    MS_EDITPROFILE_USER_FLOW = '' # B2C_1_ProfileEditPolicy
    MS_RESETPASSWORD_USER_FLOW = '' # B2C_1_Password_Reset_Policy

    # Google OAuth settings
    GOOGLE_CLIENT_ID = ''
    GOOGLE_CLIENT_SECRET = ''
    GOOGLE_DISCOVERY_URL = (
        "https://accounts.google.com/.well-known/openid-configuration"
    )
    GOOGLE_REDIRECT_URI = ''