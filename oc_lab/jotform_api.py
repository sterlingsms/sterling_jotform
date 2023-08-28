from libs.jotform.jotform import *
from .jotform_api_base import JotformAPIBase
import json
import urllib
import urllib.parse
from datetime import datetime
from pytz import timezone, utc
import pytz

class OCLab(JotformAPIBase):
    def __init__(self, api_key, arg):
        JotformAPIBase.__init__(self, api_key, arg)

    def get_order_collection_form(self,form_id=None):
        order_collection_form_link = self.base_url + "/form/" + form_id + "/source?apiKey=" + self.api_key
        get_order_collection_form_source = urllib.request.urlopen(order_collection_form_link)
        order_collection_form_source = json.loads(get_order_collection_form_source.read())
        return order_collection_form_source

    def get_pst_time(self, date_format='%m/%d/%Y %H:%M:%S'):
        date = datetime.now(tz=pytz.utc)
        date = date.astimezone(timezone('US/Pacific'))
        pstDateTime = date.strftime(date_format)
        return pstDateTime

    def get_summary(self, submission_data):
        get_lab_tests = get_name = get_vitals = summary2 = ''
        if '15' in submission_data['answers'].keys() and 'answer' in submission_data['answers']['15'].keys():
            get_lab_tests = submission_data['answers']['15']['answer'].split("\r\n")
        if '8' in submission_data['answers'].keys() and 'answer' in submission_data['answers']['8'].keys():
            get_name = submission_data['answers']['8']['answer']
        if '48' in submission_data['answers'].keys() and 'answer' in submission_data['answers']['48'].keys():
            get_vitals = submission_data['answers']['48']['answer']
        summary = 'Lab Order Request for: <strong>'+get_name+'</strong><br><br>'+'<strong>Vitals Requested:</strong> '+get_vitals+'<br><br>'
        #summary2 = 'Lab Order Request for: <strong>'+get_name+'</strong><br><br>'
        summary2 += '<strong>Specimen Collection Items Requested:</strong><br><br>'
        if len(get_lab_tests) >= 1:
            for i in get_lab_tests:
                summary2 += '- ' + i +  ' Requested' + '<br>'
        return {'summary':summary,'summary2':summary2}

    def get_log_table(self, collection_log=[], patient_name=None, vital=False):
        getrow = getrow2 = ""
        gettabe = gettabe2 = ""
        v=0
        s=0
        if len(collection_log) >= 1:
            for i in range(0, len(collection_log)):
                height = weight = bmi = bmi_readout = temperture = blood_presure = blood_presure_readout = bpm = respiration = experiencing_pain = experiencing_pain_on = completed_by = ""
                if (v >= 7 or vital == False) and s >= 7:break
                if '4' in collection_log[i]['answers'].keys() and 'answer' in collection_log[i]['answers']['4'].keys() and collection_log[i]['answers']['4']['answer'] != patient_name:continue

                x = collection_log[i]['created_at']
                # pstDate = datetime.strptime(str(x),"%Y-%m-%d %H:%M:%S")
                # pstDateTime = pstDate.strftime('%m/%d/%Y %H:%M:%S')
                pstDateTime = self.pst_time(str(x))
                # datetime.strptime(str(collection_log[i]['created_at']),"%m/%d/%Y %H:%M:%S")
                if '30' in collection_log[i]['answers'].keys() and 'answer' in collection_log[i]['answers']['30'].keys():
                    completed_by = collection_log[i]['answers']['30']['answer']


                if s < 7 and'24' in collection_log[i]['answers'].keys() and 'answer' in collection_log[i]['answers']['24'].keys():
                    specimen_collection_json = collection_log[i]['answers']['24']['answer']
                    specimens = json.loads(specimen_collection_json)
                    for specimen in specimens:
                        specimen_type = specimen_quantity = date_collected = time_collected = ""
                        date_str = specimen['Date Collected']
                        time_str = specimen['Time Collected']
                        dt_str = f"{date_str} {time_str}"
                        dt = datetime.strptime(dt_str, '%m-%d-%Y %I:%M %p')
                        date_collected = dt.strftime('%m/%d/%Y')
                        time_collected = dt.strftime('%I:%M %p')
                        specimen_type = specimen['Specimen Type']
                        specimen_quantity = specimen['Specimen Quantity']
                        getrow2 += "<tr><td>" + pstDateTime + "</td><td>" + specimen_type + "</td><td>" + specimen_quantity + "</td><td>" + date_collected + "</td><td>" + time_collected + "</td><td>" + completed_by + "</td></tr>"
                        s = s + 1

                
                if vital and v < 7:
                    if '11' in collection_log[i]['answers'].keys() and 'answer' in collection_log[i]['answers']['11'].keys():
                        weight = collection_log[i]['answers']['11']['answer']
                    if '12' in collection_log[i]['answers'].keys() and 'answer' in collection_log[i]['answers']['12'].keys():
                        temperture = collection_log[i]['answers']['12']['answer']
                    if '13' in collection_log[i]['answers'].keys() and 'answer' in collection_log[i]['answers']['13'].keys():
                        blood_presure = collection_log[i]['answers']['13']['answer']
                    if '14' in collection_log[i]['answers'].keys() and 'answer' in collection_log[i]['answers']['14'].keys():
                        bpm = collection_log[i]['answers']['14']['answer']
                    if '15' in collection_log[i]['answers'].keys() and 'answer' in collection_log[i]['answers']['15'].keys():
                        respiration = collection_log[i]['answers']['15']['answer']
                    if '16' in collection_log[i]['answers'].keys() and 'answer' in collection_log[i]['answers']['16'].keys():
                        experiencing_pain_on = ' ('+collection_log[i]['answers']['16']['answer']+')' if collection_log[i]['answers']['16']['answer'] != '' else ''
                    if '32' in collection_log[i]['answers'].keys() and 'answer' in collection_log[i]['answers']['32'].keys():
                        experiencing_pain = collection_log[i]['answers']['32']['answer']
                    if '33' in collection_log[i]['answers'].keys() and 'answer' in collection_log[i]['answers']['33'].keys():
                        height = collection_log[i]['answers']['33']['answer']
                    if '42' in collection_log[i]['answers'].keys() and 'answer' in collection_log[i]['answers']['42'].keys():
                        bmi_readout = collection_log[i]['answers']['42']['answer']
                    if '43' in collection_log[i]['answers'].keys() and 'answer' in collection_log[i]['answers']['43'].keys():
                        blood_presure_readout = collection_log[i]['answers']['43']['answer']
                    if '44' in collection_log[i]['answers'].keys() and 'answer' in collection_log[i]['answers']['44'].keys():
                        bmi = collection_log[i]['answers']['44']['answer']
                    
                    if weight != '' or temperture != '' or blood_presure != '' or bpm != '' or respiration != '':
                        getrow += "<tr><td>" + pstDateTime + "</td><td>" + height + "</td><td>" + weight + "</td><td>" + bmi + "</td><td>" + bmi_readout + "</td><td>" + temperture + "</td><td>" + blood_presure + "</td><td>" + blood_presure_readout + "</td><td>" + bpm + "</td><td>" + respiration + "</td><td>" + experiencing_pain + experiencing_pain_on + "</td><td>" + completed_by + "</td></tr>"
                        v = v + 1

        if getrow != '':
            gettabe = "<br><br><strong>Recent Records</strong><br><br><div class='table-responsive'><table class='table table-bordered table-hover'><tr><th> Date </th><th> Height </th><th> Weight </th><th> BMI Index </th><th> BMI Readout </th><th> Temp </th><th> BP </th><th> BP Readout </th><th> BPM </th><th> Respiration </th><th> Pain </th><th> " \
                      "Completed By </th></tr>" + getrow + "</table></div>"
        if getrow2 != '':
            gettabe2 = "<br><strong>Recent Records</strong><br><br><div class='table-responsive'><table class='table table-bordered table-hover'><tr><th> Date </th><th> Specimen Type </th><th> Specimen Quantity </th><th> Date Collected </th><th> Time Collected </th><th> " \
                      "Completed By </th></tr>" + getrow2 + "</table></div>"

        return {'gettabe':gettabe,'gettabe2':gettabe2}

    def get_submissions_log(self,form_id,submission_filter={}):
        # Patient name - q4 in collection form
        tdate = self.get_pst_time("%Y-%m-%d")  # datetime.today().strftime('%Y-%m-%d')
        # "created_at:gt": tdate + " 00:00:00"
        medication_log = self.get_submissions_data(form_id, None, None, submission_filter, None)
        return medication_log

    def pst_time(self, date_time = None, date_format='%m/%d/%Y %H:%M:%S'):
        # Convert EST to datetime object
        time_str = date_time
        est = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
        est_tz = timezone('US/Eastern')
        est_dt = est_tz.localize(est)

        # Convert EST to PST
        pst_tz = timezone('US/Pacific')
        pst_dt = est_dt.astimezone(pst_tz)

        # Convert PST datetime back to string
        pst_str = pst_dt.strftime('%Y-%m-%d %H:%M:%S')
        return pst_str

    def get_dynamic_data(self,form_id=None,sid=None):
        submission_data = self.get_submission_data(sid)
        order_collection_form_source = self.get_order_collection_form(form_id)
        get_summary = self.get_summary(submission_data)
        get_vitals = get_patient_name = get_physician_name = ''
        # Patient name question id - q8
        if '56' in submission_data['answers'].keys() and 'answer' in submission_data['answers']['56'].keys():
            get_patient_name = submission_data['answers']['56']['answer']
        if '9' in submission_data['answers'].keys() and 'answer' in submission_data['answers']['9'].keys():
            get_physician_name = submission_data['answers']['9']['answer']
        if '48' in submission_data['answers'].keys() and 'answer' in submission_data['answers']['48'].keys():
            get_vitals = submission_data['answers']['48']['answer']
        if get_patient_name == '' and '8' in submission_data['answers'].keys() and 'answer' in submission_data['answers']['8'].keys():
            get_patient_name = submission_data['answers']['8']['answer']
        get_vital = True if get_vitals == 'YES' else False
        """submission_filter = {"4:eq": get_patient_name}

        order_collection_submission = self.get_submissions_log(form_id,submission_filter)
        collection_log_table = self.get_log_table(order_collection_submission,get_patient_name,get_vital)
        vitals_summary = get_summary['summary']+collection_log_table['gettabe'] if get_vital else get_summary['summary']"""

        response = {
            "patient_name": get_patient_name,
            "physician_name": get_physician_name,
            "submission_data": submission_data,
            "summary": get_summary['summary']+get_summary['summary2'],#vitals_summary,
            #"summary2": get_summary['summary2']+collection_log_table['gettabe2'],
            "get_vital": get_vital,
            #"submissions_log_table": order_collection_submission,
            "order_collection_form_source": order_collection_form_source['content'],
            "tdate": self.get_pst_time('%Y-%m-%d')
        }
        return response

    def get_physician_data(self,form_id=None,sid=None):
            #submission_data = self.get_submission_data(sid)
            submissions_data = self.get_submissions_log(form_id)
            physician_data = self.get_submission_data(sid)
            patients = physician_names = get_physician_name = get_physician_license = get_physician_npi = ''
            if '8' in physician_data['answers'].keys() and 'answer' in physician_data['answers']['8'].keys():
                patient_names = json.loads(physician_data['answers']['8']['options_array']);
                #values = [val["value"] for key, val in patient_names.items()]
                patient_ids = physician_data['answers']['8']['answer']
                pids = [patient_names[pid.replace('{', '').replace('}', '')]["value"] for pid in patient_ids]
                patients = "|".join(pids)

            question_data_56 = self.get_form_question_data(form_id,qid='56')
            question_data_8 = self.get_form_question_data(form_id,qid='8')

            question_properties_56 = question_data_56
            question_properties_8 = question_data_8
            question_properties_8['items'] = question_properties_56['options'] = patients
            updated_question_56 = self.update_form_question_data(form_id,qid='56',question_properties=question_properties_56)
            updated_question_8 = self.update_form_question_data(form_id,qid='8',question_properties=question_properties_8)
            
            # Physician name question id - q51
            if len(submissions_data) > 0 and '58' in submissions_data[0]['answers'].keys() and 'options_array' in submissions_data[0]['answers']['58'].keys():
                physician_names = json.loads(submissions_data[0]['answers']['58']['options_array']);
            if '1' in physician_data['answers'].keys() and 'prettyFormat' in physician_data['answers']['1'].keys():
                get_physician_name = physician_data['answers']['1']['prettyFormat']
            if '11' in physician_data['answers'].keys() and 'answer' in physician_data['answers']['11'].keys():
                get_physician_npi = physician_data['answers']['11']['answer']
            if '12' in physician_data['answers'].keys() and 'answer' in physician_data['answers']['12'].keys():
                get_physician_license = physician_data['answers']['12']['answer']

            response = {
                "physician_name": get_physician_name,
                "physician_npi": get_physician_npi,
                "physician_license": get_physician_license,
                "physician_data":physician_data,
                "patient_names":patients,
                "sid":physician_names
            }
            return response

    def clear_request_form_data(self,form_id=None):
            question_data_56 = self.get_form_question_data(form_id,qid='56')
            question_data_8 = self.get_form_question_data(form_id,qid='8')

            question_properties_56 = question_data_56
            question_properties_8 = question_data_8
            question_properties_8['items'] = question_properties_56['options'] = ""
            updated_question_56 = self.update_form_question_data(form_id,qid='56',question_properties=question_properties_56)
            updated_question_8 = self.update_form_question_data(form_id,qid='8',question_properties=question_properties_8)
            
            response = {
                "question_56": updated_question_56,
                "question_8":updated_question_8,
            }
            return response

    def get_register_physician_data(self,form_id=None,nfcid=None):
            submission_filter = {"9:eq": nfcid}
            get_physician_data = {}
            physician_data = self.get_submissions_data(formID=form_id, offset=None, limit=None, filterArray=submission_filter)
            if len(physician_data) >= 1:
                for i in range(0, len(physician_data)):
                    if '9' in physician_data[i]['answers'].keys() and 'answer' in physician_data[i]['answers']['9'].keys() and physician_data[i]['answers']['9']['answer'] == nfcid: 
                        get_physician_data = physician_data[i];

            response = {
                "physician_data":get_physician_data,
                "nfcid":nfcid
            }
            return response