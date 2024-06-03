import pandas as pd
import json
from datetime import datetime
from flask import render_template, jsonify, session, redirect
from application import app
from application.controller.user import user_check_index
from application.model import project as project_db


def home_index(templ_html, project_id):
    try:
        reg_usr = '/user/register'
        log_usr = '/user/login'
        lg_ms = '/user/login/microsoft'
        lg_google = '/user/login/google'
        lg_logout = '/user/logout'
        lg_profile = '/user/profile'
        lg_user = session['user'] if session.get('user') else None
        lg_user = session['_logged_in_user'] if (lg_user is None and session.get('_logged_in_user')) else lg_user
        session['user'] = lg_user

        if (lg_user is not None):
            user_check_index()

        if (project_id is not None):
            project_db_extr = project_db.Project.query.filter_by(id=project_id).first()
            session['view_project'] = project_db_extr
            prj_table_columns = list(dict.fromkeys(list(map(lambda x: x.column_name, project_db_extr.project_tables))))
            prj_table_json = {}
            for cl in prj_table_columns:
                prj_table_cls = list(filter(lambda x: x.column_name == cl, project_db_extr.project_tables))
                prj_table_cls = sorted(prj_table_cls, key=lambda x: x.row_index, reverse=False)
                prj_table_json[cl] = {}
                for i, obj in enumerate(prj_table_cls):
                    prj_table_json[cl][str(obj.row_index)] = \
                        int(obj.column_value) if obj.column_value.isnumeric() and obj.column_value.isdigit() \
                        else float(obj.column_value) if obj.column_value.isnumeric() and not obj.column_value.isdigit() \
                        else obj.column_value
            data = json.dumps(prj_table_json)
            data = pd.read_json(data)
            session['uploaded_file_data'] = data
            session['uploaded_file_data_html'] = data.to_html()
            session['uploaded_file_data_json'] = data.to_json(force_ascii=False)
        else:
            session['view_project'] = None

        return render_template(templ_html,
                               register_account=reg_usr,
                               login_account=log_usr,
                               login_microsoft=lg_ms,
                               login_google=lg_google,
                               logout=lg_logout,
                               account_profile=lg_profile,
                               user=lg_user)
    except Exception as ex:
        return redirect('/')


def page_not_found_index(error):
    return render_template('static/404.html'), 404