import os
import pandas as pd
from flask import Flask, render_template, jsonify, request, redirect, session
from fileinput import filename
from pyarxaas import ARXaaS, AttributeType, Dataset
from pyarxaas.privacy_models import KAnonymity
from pyarxaas.hierarchy import IntervalHierarchyBuilder, OrderHierarchyBuilder, DateHierarchyBuilder, RedactionHierarchyBuilder
from config import Config

documents_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'documents'))
xlsx_content_types = ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/vnd.ms-excel']
csv_content_types = ['.csv']

arxaas = None
try:
    arxaas = ARXaaS(Config.APP_ARXaaS_URL)
except Exception:
    print(Exception)

def data_upload_excel():
    # Read the File using Flask request
    file = request.files['file']
    # save file in local directory
    file.save(os.path.join(documents_path, file.filename))

    # Parse the data as a Pandas DataFrame type
    data = pd.read_excel(file) if (file.content_type in xlsx_content_types) else \
        pd.read_csv(file, sep=',', encoding='unicode_escape', index_col=0, on_bad_lines="warn")
    data.fillna(0, inplace=True)
    session['uploaded_file_data'] = data
    session['uploaded_file_data_html'] = data.to_html()
    session['uploaded_file_data_json'] = data.to_json(force_ascii=False)

    # Return HTML snippet that will render the table
    return redirect('/')


def anonymize_data(args):
    data = session['uploaded_file_data']
    dataset = Dataset.from_pandas(data)

    # get the risk profle of the dataset
    risk_profile = arxaas.risk_profile(dataset)
    # get risk metrics
    na_re_indentification_risk = risk_profile.re_identification_risk
    na_rp_attacker_success_rate = risk_profile.attacker_success_rate
    na_distribution_of_risk = risk_profile.distribution_of_risk

    # intervalH = IntervalHierarchyBuilder.add_interval(IntervalHierarchyBuilder, 0, 10, '*')
    no_config_redaction_based = RedactionHierarchyBuilder()  # Create builder
    order_based = OrderHierarchyBuilder()
    # set attribute type
    # dataset.set_attribute_type(AttributeType.QUASIIDENTIFYING, 'VisitorCardNbr', 'VisitorEmail')
    # dataset.set_attribute_type(AttributeType.IDENTIFYING, 'Invitor')
    # redaction_hierarchy = arxaas.hierarchy(no_config_redaction_based, data['VisitorCardNbr'].tolist())
    # dataset.set_hierarchy('VisitorCardNbr', no_config_redaction_based)
    # dataset.set_hierarchy('VisitorEmail', no_config_redaction_based)
    # dataset.set_hierarchy('VisitorCardNbr', intervalH)
    # dataset.set_hierarchy('VisitorEmail', intervalH)

    # dataset.set_attribute_type(AttributeType.IDENTIFYING, "Invitor")
    dataset.set_attribute_type(AttributeType.QUASIIDENTIFYING, 'Type', 'Invitor', 'Invitor_FullName', 'VisitorName')
    redaction_hierarchy = arxaas.hierarchy(no_config_redaction_based, data['Type'].tolist())
    dataset.set_hierarchy("Type", redaction_hierarchy)
    redaction_hierarchy = arxaas.hierarchy(no_config_redaction_based, data['Invitor'].tolist())
    dataset.set_hierarchy("Invitor", redaction_hierarchy)
    redaction_hierarchy = arxaas.hierarchy(no_config_redaction_based, data['Invitor_FullName'].tolist())
    dataset.set_hierarchy("Invitor_FullName", redaction_hierarchy)
    redaction_hierarchy = arxaas.hierarchy(no_config_redaction_based, data['VisitorName'].tolist())
    dataset.set_hierarchy("VisitorName", redaction_hierarchy)

    kanon = KAnonymity(2)
    anonymize_result = arxaas.anonymize(dataset, [kanon])

    # get the new dataset
    anonymized_dataset = anonymize_result.dataset
    anon_dataframe = anonymized_dataset.to_dataframe()
    session['annonymized_file_data'] = anon_dataframe
    session['annonymized_file_data_html'] = anon_dataframe.to_html()
    session['annonymized_file_data_json'] = anon_dataframe.to_json(force_ascii=False)

    # get the risk profile for the new dataset
    anon_risk_profile = anonymize_result.risk_profile

    # get risk metrics as a dictionary
    a_re_indentification_risk = anon_risk_profile.re_identification_risk
    a_rp_attacker_success_rate = anon_risk_profile.attacker_success_rate
    a_distribution_of_risk = anon_risk_profile.distribution_of_risk

    # get risk metrivs as pandas.DataFrame
    re_i_risk_df = anon_risk_profile.distribution_of_risk_dataframe()
    dist_risk_df = anon_risk_profile.distribution_of_risk_dataframe()

    # get the anonymiztion metrics
    anon_metrics = anonymize_result.anonymization_metrics

    print(args)
    return jsonify({
        'status': 'success',
        'non_anonymized': {
            'indentification_risk': na_re_indentification_risk,
            'attacker_success_rate': na_rp_attacker_success_rate,
            'distribution_of_risk': na_distribution_of_risk
        },
        'anonymized': {
            'indentification_risk': a_re_indentification_risk,
            'attacker_success_rate': a_rp_attacker_success_rate,
            'distribution_of_risk': a_distribution_of_risk
        }
    })

