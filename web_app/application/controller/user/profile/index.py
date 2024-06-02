from datetime import datetime
from flask import render_template, jsonify, session, redirect
from swiftcrypt import swiftcrypt

from application.controller import home, user
from application.model import user as user_db
from application import app, db


def user_login_profile_index():
    return "Welcome to Route profile NEW!"


def user_register(request, args):
    if (session['user']):
        return redirect('/')
    else:
        responseJSON = {
            'status': None,
            'message': None,
            'username': None,
            'token': None
        }
        if (request.method == 'GET'):
            return home.home_index('user/register.html')
        if (request.method == 'POST'):
            db_user_check = user_db.User.query.filter_by(username=args.get("username")).first()
            if (db_user_check is None):
                password = args.get('password')
                repeat_password = args.get('repeat_password')
                if (password == repeat_password):
                    salt = swiftcrypt.Salts().generate_salt(16).encode('utf-8').hex()
                    hashedPass = swiftcrypt.Hash().hash_password(password, salt, 'sha512')

                    new_record = user_db.User()
                    new_record.login_type = 'user'
                    new_record.username = args.get("username")
                    new_record.password = hashedPass
                    new_record.salt = salt
                    new_record.role = 'STD'
                    new_record.name = args.get("name")
                    new_record.address = args.get("address")
                    new_record.phone_nbr = args.get("phone_nbr")
                    new_record.created_at = datetime.now()

                    db.session.add(new_record)
                    db.session.commit()

                    user_info = {
                        'username': args.get("username"),
                        'name': args.get("name"),
                        'logged_in_usertype': 'std_user'
                    }
                    session['user'] = user_info
                    responseJSON['status'] = 'success'
                else:
                    responseJSON['status'] = 'fail'
                    responseJSON['message'] = 'Passwords do not match'
            else:
                responseJSON['status'] = 'fail'
                responseJSON['message'] = 'User already exists'
        else:
            responseJSON['status'] = 'fail'
            responseJSON['message'] = 'Non acceptable URL method'

        return jsonify(responseJSON)


def user_login(request, args):
    if (session['user']):
        return redirect('/')
    else:
        responseJSON = {
            'status': None,
            'message': None,
            'username': None,
            'token': None
        }
        if (request.method == 'GET'):
            return home.home_index('user/login.html')
        if (request.method == 'POST'):
            db_user_check = user_db.User.query.filter_by(username=args.get("username")).first()
            if (db_user_check is not None):
                hashedPass = swiftcrypt.Hash().hash_password(args.get("password"), db_user_check.salt, 'sha512')
                if (hashedPass == db_user_check.password):
                    responseJSON['status'] = 'success'
                    user_info = {
                        'username': db_user_check.username,
                        'name': db_user_check.name,
                        'logged_in_usertype': 'std_user'
                    }
                    session['user'] = user_info
                else:
                    responseJSON['status'] = 'fail'
                    responseJSON['message'] = 'Passwords do not match'
            else:
                responseJSON['status'] = 'fail'
                responseJSON['message'] = 'User does not exist'

            return jsonify(responseJSON)
