from datetime import datetime
from flask import render_template, jsonify, session, redirect
import json
from application.model import user as user_db,\
    project as project_db,\
    project_table as project_table_db,\
    data_transformation as data_transformation_db,\
    privacy_model as privacy_model_db
from application import app, db


def project_modify(request, args):
    c_username = session['user_email'] if 'user_email' in session else None

    if (c_username is None):
        return jsonify({
            'status': 'fail',
            'message': 'No logged in user. Please login again'
        })
    else:
        c_project_id = args.get('project_id')
        c_project_name = args.get('project_name')
        db_user_check = user_db.User.query.filter_by(username=c_username).first()

        # Check project
        db_project_extr = project_db.Project.query.filter_by(id=c_project_id, user_id=db_user_check.id).first()
        if (db_project_extr is None):
            db_project_extr = project_db.Project()
            db_project_extr.name = c_project_name
            db_project_extr.user_id = db_user_check.id
            db_project_extr.updated_at = datetime.now()
            db_project_extr.created_at = datetime.now()

            db.session.add(db_project_extr)
        else:
            db_project_extr.name = c_project_name
            db_project_extr.updated_at = datetime.now()
            db.session.add(db_project_extr)

        db.session.commit()

        # Check project table
        project_table_db_extr = project_table_db.ProjectTable\
            .query\
            .filter_by(project_id=db_project_extr.id)\
            .all()

        if (len(project_table_db_extr) > 0):
            for d_obj in project_table_db_extr:
                db.session.delete(d_obj)
        p_table = json.loads(session['uploaded_file_data'].to_json(force_ascii=False))
        for i, obj in enumerate(p_table):
            for ind in p_table[obj]:
                project_table_db_extr = None
                project_table_db_extr = project_table_db.ProjectTable()
                project_table_db_extr.project_id = db_project_extr.id
                project_table_db_extr.row_index = int(ind)
                project_table_db_extr.column_type = 'tbody'
                project_table_db_extr.column_name = obj
                project_table_db_extr.column_value = p_table[obj][ind]
                project_table_db_extr.updated_at = datetime.now()
                project_table_db_extr.created_at = datetime.now()

                db.session.add(project_table_db_extr)

        # Check data transformation
        data_transformation_db_extr = data_transformation_db.ProjectDataTransformation\
            .query\
            .filter_by(project_id=db_project_extr.id)\
            .all()
        if (len(data_transformation_db_extr) > 0):
            for d_obj in data_transformation_db_extr:
                db.session.delete(d_obj)
        for (ind, obj) in enumerate(args.get('transformation_data').get('data_transformation')):
            data_transformation_db_extr = data_transformation_db.ProjectDataTransformation()
            data_transformation_db_extr.project_id = db_project_extr.id
            data_transformation_db_extr.column_name = obj['Column_Name']
            data_transformation_db_extr.column_type = obj['Column_Type']
            data_transformation_db_extr.transformation_type = obj['Transformation_Type']
            data_transformation_db_extr.hierarchy_type = obj['Hierarchy_Type']
            data_transformation_db_extr.hierarchy_symbols = obj['Hierarchy_Symbols']
            data_transformation_db_extr.updated_at = datetime.now()
            data_transformation_db_extr.created_at = datetime.now()

            db.session.add(data_transformation_db_extr)

        # db.session.commit()

        # Check privacy model
        privacy_model_db_extr = privacy_model_db.ProjectPrivacyModel\
            .query\
            .filter_by(project_id=db_project_extr.id)\
            .all()
        if (len(privacy_model_db_extr) > 0):
            for d_obj in privacy_model_db_extr:
                db.session.delete(d_obj)
        for (ind, obj) in enumerate(args.get('transformation_data').get('privacy_model')):
            privacy_model_db_extr = privacy_model_db.ProjectPrivacyModel()
            privacy_model_db_extr.project_id = db_project_extr.id
            privacy_model_db_extr.column_name = obj['Column_Name']
            privacy_model_db_extr.column_type = obj['Column_Type']
            privacy_model_db_extr.column_privacy_model = obj['Privacy_Model']
            privacy_model_db_extr.column_value = obj['Value']
            privacy_model_db_extr.updated_at = datetime.now()
            privacy_model_db_extr.created_at = datetime.now()

            db.session.add(privacy_model_db_extr)

        db.session.commit()

        return jsonify({
            'status': 'success',
            'project_id': db_project_extr.id
        })


def project_delete(request, args):
    c_username = session['user_email'] if 'user_email' in session else None

    if (c_username is None):
        return jsonify({
            'status': 'fail',
            'message': 'No logged in user. Please login again'
        })
    else:
        c_project_id = args.get('project_id')
        db_user_check = user_db.User.query.filter_by(username=c_username).first()
        db_project_extr = project_db.Project.query.filter_by(id=c_project_id, user_id=db_user_check.id).first()
        if (db_project_extr is None):
            return jsonify({
                'status': 'fail',
                'message': 'Not equal creation user to project'
            })
        else:
            for d_obj in db_project_extr.project_privacy_models:
                db.session.delete(d_obj)
            for d_obj in db_project_extr.project_data_transformations:
                db.session.delete(d_obj)
            for d_obj in db_project_extr.project_tables:
                db.session.delete(d_obj)
            db.session.delete(db_project_extr)
            db.session.commit()
            return jsonify({
                'status': 'success',
                'message': 'Project is deleted'
            })
