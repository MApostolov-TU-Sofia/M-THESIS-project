from datetime import datetime
from flask import render_template, request
from application import app
from application.controller.home import home_index, page_not_found_index


@app.route('/', defaults={'project_id': None})
@app.route('/<project_id>')
def home_route(project_id):
    return home_index('home/index.html', project_id)


@app.errorhandler(404)
def page_not_found(error):
    return page_not_found_index(error)

