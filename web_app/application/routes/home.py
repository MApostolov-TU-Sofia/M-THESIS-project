from datetime import datetime
from flask import render_template, request
from application import app
from application.controller.home import home_index, page_not_found_index


@app.route('/')
def home_route():
    return home_index()


@app.errorhandler(404)
def page_not_found(error):
    return page_not_found_index(error)

