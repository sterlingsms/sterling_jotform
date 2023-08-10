from flask import current_app
from .jotform_api import OCLab
from APIException import APIException
import os
import json

def get_oclab_data(sid):
    if sid:
        # Lab Order Form : Form ID - 231364985876069
        # Access the configuration settings
        arg = {'base_url': current_app.config['JOTFORM_API_BASE_TEAM_URL'], "team_id": current_app.config['TEAM_ID']}
        api_key = current_app.config['API_KEY']
        oc_lab = OCLab(api_key, arg)
        data = oc_lab.get_dynamic_data(current_app.config['OC_FORM_ID'],sid)
        return data
    else:
    	raise APIException('Invalid request - Query parameter sid is missing', status_code=400)

def get_oclab_order_data(sid):
    if sid:
        # Lab Order Form : Form ID - 231364985876069
        # Access the configuration settings
        arg = {'base_url': current_app.config['JOTFORM_API_BASE_TEAM_URL'], "team_id": current_app.config['TEAM_ID']}
        api_key = current_app.config['API_KEY']
        oc_lab = OCLab(api_key, arg)
        physician_data = oc_lab.get_physician_data(current_app.config['OC_REQUEST_FORM_ID'],sid)
        # Loading variables from file
        html_string = ''
        # Path to the file
        file_path = "oc_lab/data/form_order_request.txt"

        # Get the absolute path of the file
        absolute_path = os.path.abspath(file_path)

        # Print the absolute path of the file
        with open('oc_lab/data/form_order_request.txt', 'r') as html_file:
            html_string = html_file.read()
        iframe_src = current_app.config['JOTFORM_EP_BASE_URL']+current_app.config['OC_REQUEST_FORM_ID']+"?PhysicianName="+physician_data['physician_name']+"&isIframeEmbed=1"
        html_string_up = html_string.replace("__IFRAME_SRC__", iframe_src)
        response = {'content':html_string_up,"physician_data":physician_data,"iframe_src":iframe_src}
        return response
    else:
        raise APIException('Invalid request - Query parameter sid is missing', status_code=400)

def get_oclab_order_request_hook(reqData):
    if reqData:
        # Lab Order request Form : Form ID - 231296684863065
        # Access the configuration settings
        arg = {'base_url': current_app.config['JOTFORM_API_BASE_TEAM_URL'], "team_id": current_app.config['TEAM_ID']}
        api_key = current_app.config['API_KEY']
        oc_lab = OCLab(api_key, arg)
        response = oc_lab.clear_request_form_data(current_app.config['OC_REQUEST_FORM_ID'])
        return response
    else:
        raise APIException('Invalid request', status_code=400)

def get_provider_register_data(nfcid):
    if nfcid:
        # Lab Order Form : Form ID - 231364985876069
        # Access the configuration settings
        arg = {'base_url': current_app.config['JOTFORM_API_BASE_TEAM_URL'], "team_id": current_app.config['TEAM_ID']}
        api_key = current_app.config['API_KEY']
        re_url = nfc = ''
        oc_lab = OCLab(api_key, arg)
        physician_data = oc_lab.get_register_physician_data(current_app.config['OC_PROVIDER_REGISTER_FORM_ID'],nfcid)
        if physician_data['physician_data']:
            re_url = current_app.config['OC_REQUEST_FORM_SS']+physician_data['physician_data']['id']
            nfc = physician_data['physician_data']['answers']['9']['answer']

        response = {"content":{"nfcid":nfc,'re_url':re_url}}
        return response
    else:
        raise APIException('Invalid request - Query parameter nfcid is missing', status_code=400)
