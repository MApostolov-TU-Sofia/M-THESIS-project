import os
import pandas
from flask import Flask, render_template, request, redirect, session
from fileinput import filename

documents_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'documents'))
xlsx_content_types = ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/vnd.ms-excel']
csv_content_types = ['.csv']


def data_upload_excel():
    # Read the File using Flask request
    file = request.files['file']
    # save file in local directory
    file.save(os.path.join(documents_path, file.filename))

    # Parse the data as a Pandas DataFrame type
    data = pandas.read_excel(file) if (file.content_type in xlsx_content_types) else \
        pandas.read_csv(file, sep=',', encoding='unicode_escape', index_col=0, on_bad_lines="warn")
    session['uploaded_file_data_html'] = data.to_html()
    session['uploaded_file_data_json'] = data.to_json(force_ascii=False)

    # Return HTML snippet that will render the table
    return redirect('/')