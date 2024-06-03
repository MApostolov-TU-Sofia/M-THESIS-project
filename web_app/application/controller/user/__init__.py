from flask import Flask, redirect, url_for, render_template, session
from application.model import user as user_db
from application import app, db
from datetime import datetime


def user_check_index():
    c_user_info = session['user']
    if (c_user_info is not None):
        user_email = c_user_info.get("email") if (c_user_info.get("email") is not None) else None
        user_email = c_user_info.get("preferred_username") if (user_email is None and c_user_info.get("preferred_username") is not None) else user_email

        user_type = 'google' if (c_user_info.get("iss") is not None and 'google' in c_user_info.get("iss")) else None
        user_type = 'microsoft' if (c_user_info.get("iss") is not None and 'microsoft' in c_user_info.get("iss")) else user_type
        user_type = 'std' if (user_type is None) else user_type

        user_name = c_user_info.get('name') if (c_user_info.get("iss") is not None and 'microsoft' in c_user_info.get("iss")) else None
        user_name = c_user_info.get('name') if (c_user_info.get("iss") is not None and 'google' in c_user_info.get("iss")) else user_name

        session['user_email'] = user_email
        if (user_email is not None):
            db_user_check = user_db.User.query.filter_by(username=user_email).first()
            if (not db_user_check):
                new_record = user_db.User()
                new_record.login_type = user_type
                new_record.username = user_email
                new_record.password = ''
                new_record.salt = ''
                new_record.role = 'STD'
                new_record.name = user_name
                new_record.address = None
                new_record.phone_nbr = None
                new_record.created_at = datetime.now()

                db.session.add(new_record)
                db.session.commit()
                print(user_email + ' added')