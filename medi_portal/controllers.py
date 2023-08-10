from flask import current_app
from .jotform_api import MedicationLog
from APIException import APIException

def get_intake_data(sid):
    if sid:
        # Medication Log : Form ID - 223625492681057
        # Access the configuration settings
        arg = {'base_url': current_app.config['JOTFORM_API_BASE_TEAM_URL'], "team_id": current_app.config['TEAM_ID']}
        api_key = current_app.config['API_KEY']
        medication_log = MedicationLog(api_key, arg)
        data = medication_log.get_dynamic_data(current_app.config['MEDI_FORM_ID'],sid)
        return data
    else:
    	raise APIException('Invalid request - Query parameter sid is missing', status_code=400)
