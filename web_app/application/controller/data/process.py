import os
import pandas as pd
from flask import Flask, render_template, jsonify, request, redirect, session
from fileinput import filename
from pyarxaas import ARXaaS, AttributeType, Dataset
from pyarxaas.privacy_models import KAnonymity, LDiversityDistinct, TClosenessEqualDistance
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
    try:
        data = session['uploaded_file_data']
        dataset = Dataset.from_pandas(data)

        # get the risk profle of the dataset
        risk_profile = arxaas.risk_profile(dataset)
        # get risk metrics
        na_re_indentification_risk = risk_profile.re_identification_risk
        na_rp_attacker_success_rate = risk_profile.attacker_success_rate
        na_distribution_of_risk = risk_profile.distribution_of_risk

        for ind, dts in enumerate(args['data_transformation']):
            c_attr = AttributeType.IDENTIFYING if (dts['Transformation_Type'] == 'identifying') else AttributeType.QUASIIDENTIFYING if (dts['Transformation_Type'] == 'quasi_identifying') else AttributeType.SENSITIVE if (dts['Transformation_Type'] == 'sensitive') else AttributeType.INSENSITIVE if (dts['Transformation_Type'] == 'insensitive') else None
            if (c_attr is not None):
                dataset.set_attribute_type(c_attr, dts['Column_Name'])

                hierarchy_builder = RedactionHierarchyBuilder(redaction_char=dts['Hierarchy_Symbols']) if (dts['Hierarchy_Type'] == 'redaction') else IntervalHierarchyBuilder() if (dts['Hierarchy_Type'] == 'interval') else DateHierarchyBuilder() if (dts['Hierarchy_Type'] == 'date') else None

                if (dts['Hierarchy_Type'] == 'interval'):
                    i_intervals = dts['Hierarchy_Symbols'].split('|')
                    for i_ind, i_dts in enumerate(i_intervals):
                        if (len(i_dts.strip()) > 0):
                            i_dts_el = i_dts.split(',')
                            hierarchy_builder.add_interval(int(i_dts_el.get(0)), int(i_dts_el.get(1)), i_dts_el.get(2))
                if (hierarchy_builder is not None):
                    redaction_hierarchy = arxaas.hierarchy(hierarchy_builder, data[dts['Column_Name']].tolist())
                    dataset.set_hierarchy(dts['Column_Name'], redaction_hierarchy)

        arr_anon = []
        for ind, dts in enumerate(args['privacy_model']):
            t_anon = KAnonymity(int(dts['Value'])) if (dts['Privacy_Model'] == 'KAnonymity') else LDiversityDistinct(int(dts['Value']), dts['Column_Name']) if (dts['Privacy_Model'] == 'LDiversity') else TClosenessEqualDistance(float(dts['Value']), dts['Column_Name']) if (dts['Privacy_Model'] == 'TCloseness') else None
            if (t_anon is not None):
                arr_anon.append(t_anon)

        dt_column_names = list(map(lambda x: x['Column_Name'], args['data_transformation']))
        pm_column_names = list(map(lambda x: x['Column_Name'], args['privacy_model']))

        for ind, dts in enumerate(data.columns):
            if (dts not in dt_column_names and dts not in pm_column_names):
                no_config_redaction_based = RedactionHierarchyBuilder()
                redaction_hierarchy = arxaas.hierarchy(no_config_redaction_based, data[dts].tolist())
                dataset.set_hierarchy(dts, redaction_hierarchy)

        # anonymize data
        anonymize_result = arxaas.anonymize(dataset, arr_anon)

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

        return jsonify({
            'status': 'success',
            'anonymized_data': anon_dataframe.to_html(),
            'analyze_risk': {
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
            }
        })
    except Exception as err:
        return jsonify({
            'status': 'fail',
            'message': err.args[0]
        })

