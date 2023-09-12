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

    def get_summary(self, submission_data, physician_data):
        get_lab_tests = get_lab_tests2 = pcrPanel1= pcrPanel2 = get_patient_info = get_patient_info_labels = patientInfo = subscription = patientName = vitals_tests = is_complete = get_ids_pics = get_physician_signature = get_vitals = summary2 = get_lab_tests_other = get_physician_license = get_physician_npi = get_location = ''
        if '108' in submission_data['answers'].keys() and 'prettyFormat' in submission_data['answers']['108'].keys():
            get_lab_tests = submission_data['answers']['108']['prettyFormat']
        if '112' in submission_data['answers'].keys() and 'prettyFormat' in submission_data['answers']['112'].keys():
            get_lab_tests2 = submission_data['answers']['112']['prettyFormat']
        if '111' in submission_data['answers'].keys() and 'sublabels' in submission_data['answers']['111'].keys():
            get_patient_info_labels = submission_data['answers']['111']['sublabels']
        if '110' in submission_data['answers'].keys() and 'answer' in submission_data['answers']['110'].keys():
            is_complete = submission_data['answers']['110']['answer']
        if '48' in submission_data['answers'].keys() and 'answer' in submission_data['answers']['48'].keys():
            get_vitals = submission_data['answers']['48']['answer']
        if '65' in submission_data['answers'].keys() and 'answer' in submission_data['answers']['65'].keys():
            get_lab_tests_other = submission_data['answers']['65']['answer']
        if '61' in submission_data['answers'].keys() and 'answer' in submission_data['answers']['61'].keys():
            get_location = submission_data['answers']['61']['answer']
        if physician_data != '' and '11' in physician_data['answers'].keys() and 'answer' in physician_data['answers']['11'].keys():
            get_physician_npi = physician_data['answers']['11']['answer']
        if physician_data != '' and '12' in physician_data['answers'].keys() and 'answer' in physician_data['answers']['12'].keys():
            get_physician_license = physician_data['answers']['12']['answer']
        if '75' in submission_data['answers'].keys() and 'answer' in submission_data['answers']['75'].keys():
            get_physician_signature = "<img src="+submission_data['answers']['75']['answer']+" alt="+submission_data['answers']['75']['text']+" title="+submission_data['answers']['75']['text']+">"
        if '111' in submission_data['answers'].keys() and 'answer' in submission_data['answers']['111'].keys():
            get_patient_info = submission_data['answers']['111']['answer']
        if '118' in submission_data['answers'].keys() and 'prettyFormat' in submission_data['answers']['118'].keys():
            pcrPanel1 = submission_data['answers']['118']['prettyFormat']
        if '119' in submission_data['answers'].keys() and 'prettyFormat' in submission_data['answers']['119'].keys():
            pcrPanel2 = submission_data['answers']['119']['prettyFormat']
        if '121' in submission_data['answers'].keys() and 'answer' in submission_data['answers']['121'].keys():
            vitals_tests = submission_data['answers']['121']['answer']
        if '122' in submission_data['answers'].keys() and 'answer' in submission_data['answers']['122'].keys():
            subscription = submission_data['answers']['122']['answer'][0]
        
        patient_info_labels = json.loads(get_patient_info_labels)
        if len(patient_info_labels) >= 1:
            for k,v in patient_info_labels.items():
                patientVal = get_patient_info[k] if k in get_patient_info else ''
                if v == 'Patient Name':
                    patientName = patientVal
                    continue
                patientInfo += '<tr><td>'+v+': </td><td>'+patientVal+'</td></tr>'
        patientInfo_table = "<table><tbody>"+patientInfo+"</tbody></table>"

        if is_complete == 'PENDING':
            is_complete = '<br><p class="form_status">Form Is Pending</p><br>'
        else:
            is_complete = ''

        """get_ids_pics = '<a href="" class="big" rel="rel1"><img src="" alt="ID" title="Image 1"></a>'
        get_gallery = '<div class="gallery">'+get_ids_pics+'</div>'"""
        summary = is_complete+patientInfo_table+'<br><br>'+'<strong>Vitals Requested:</strong> '+get_vitals+'<br><br>'
        if len(vitals_tests) > 0:
            vt_body = ''
            for vt in vitals_tests:
                vt_body += '<tr><td>'+vt+'</td></tr>'
            summary +="<div class='vt_container'><table><tbody>"+vt_body+"</tbody></table></div><br><br>"
        #summary2 = 'Lab Order Request for: <strong>'+get_patient_info+'</strong><br><br>'
        summary2 += '<strong>Specimen Collection Items Requested:</strong>'
        summary2 += '<br><br><strong>PCR Panel 1</strong>'+pcrPanel1 if pcrPanel1 != '' else ''
        summary2 += '<br><br><strong>PCR Panel 2</strong>'+pcrPanel2 if pcrPanel2 != '' else ''
        summary2 += '<br><br><strong>Blood Test 1</strong><div class="blood_test_tabel">'+get_lab_tests+'</div>' if get_lab_tests != '' else '</div>'
        summary2 += '<br><br><strong>Blood Test 2</strong><div class="blood_test_tabel">'+get_lab_tests2+'</div>' if get_lab_tests2 != '' else '</div>'
        summary2 += '<br><br>'+'<strong>Subscription Requested? </strong> '+subscription+'<br><br>'
        """if len(get_lab_tests) >= 1:
            for i,j in get_lab_tests.items():
                if i == 'OTHER' and get_lab_tests_other != '':
                    summary2 += '- ' + get_lab_tests_other +  ' Requested' + '<br>'
                elif j != '':
                    test_info = json.loads(j)
                    if test_info[0] != '':
                        summary2 += '- ' + i +  ' Requested ( DX Code :'+test_info[1]+ ')<br>'
        if len(get_lab_tests2) >= 1:
            for m,n in get_lab_tests2.items():
                if m == 'OTHER' and get_lab_tests_other != '':
                    summary2 += '- ' + get_lab_tests_other +  ' Requested' + '<br>'
                elif n != '':
                    test_info2 = json.loads(n)
                    if test_info2[0] != '':
                        summary2 += '- ' + m +  ' Requested ( DX Code :'+test_info2[1]+ ')<br>'"""
        summary2 += '<br><strong>Physician ID: </strong>'+get_physician_license+'<br>'+'<strong>Physician NPI ID:</strong> '+get_physician_npi+'<br>'
        summary2 += '<strong>Geo Location:</strong> <a href="'+get_location+'">Physician Location</a><br>'
        return {'summary':summary,'summary2':summary2,'patientName':patientName,'getPhysicianSignature':get_physician_signature}

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
        physician_data = ''
        submission_data = self.get_submission_data(sid)
        if '68' in submission_data['answers'].keys() and 'answer' in submission_data['answers']['68'].keys():
            get_physician_sid = submission_data['answers']['68']['answer']
            physician_data = self.get_submission_data(get_physician_sid)
        order_collection_form_source = self.get_order_collection_form(form_id)
        get_summary = self.get_summary(submission_data,physician_data)
        get_vitals = get_patient_name = get_physician_name = ''
        get_patient_name = get_summary['patientName']
        get_physician_signature = get_summary['getPhysicianSignature']
        # Patient name question id - q8 - check q56 exist or not
        if '9' in submission_data['answers'].keys() and 'answer' in submission_data['answers']['9'].keys():
            get_physician_name = submission_data['answers']['9']['answer']
        if '48' in submission_data['answers'].keys() and 'answer' in submission_data['answers']['48'].keys():
            get_vitals = submission_data['answers']['48']['answer']
        get_vital = True if get_vitals == 'YES' else False
        """submission_filter = {"4:eq": get_patient_name}

        order_collection_submission = self.get_submissions_log(form_id,submission_filter)
        collection_log_table = self.get_log_table(order_collection_submission,get_patient_name,get_vital)
        vitals_summary = get_summary['summary']+collection_log_table['gettabe'] if get_vital else get_summary['summary']"""

        response = {
            "patient_name": get_patient_name,
            "physician_name": get_physician_name,
            "submission_data": submission_data,
            "physician_data":physician_data,
            "physician_signature":get_physician_signature,
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
            patients = physician_names = get_physician_name = get_physician_license = get_physician_npi = get_degree_designation =''
            if '8' in physician_data['answers'].keys() and 'answer' in physician_data['answers']['8'].keys():
                #values = [val["value"] for key, val in patient_names.items()]
                patient_ids = physician_data['answers']['8']['answer']
                if 'options_array' in physician_data['answers']['8'].keys():
                    patient_names = json.loads(physician_data['answers']['8']['options_array']);
                    pids = [patient_names[pid.replace('{', '').replace('}', '')]["value"] for pid in patient_ids]
                    patients = "|".join(pids)            
            # Physician name question id - q51
            if len(submissions_data) > 0 and '58' in submissions_data[0]['answers'].keys() and 'options_array' in submissions_data[0]['answers']['58'].keys():
                physician_names = json.loads(submissions_data[0]['answers']['58']['options_array']);
            if '1' in physician_data['answers'].keys() and 'prettyFormat' in physician_data['answers']['1'].keys():
                get_physician_name = physician_data['answers']['1']['prettyFormat']
            if '11' in physician_data['answers'].keys() and 'answer' in physician_data['answers']['11'].keys():
                get_physician_npi = physician_data['answers']['11']['answer']
            if '12' in physician_data['answers'].keys() and 'answer' in physician_data['answers']['12'].keys():
                get_physician_license = physician_data['answers']['12']['answer']
            if '13' in physician_data['answers'].keys() and 'answer' in physician_data['answers']['13'].keys():
                get_degree_designation = ', '+', '.join(physician_data['answers']['13']['answer'])

            response = {
                "physician_name": get_physician_name,
                "physician_npi": get_physician_npi,
                "physician_license": get_physician_license,
                "degree_designation":get_degree_designation,
                "physician_data":physician_data,
                "patient_names":patients,
                "sid":physician_names
            }
            return response

    def clear_request_form_data(self,form_id=None):
            question_data_8 = self.get_form_question_data(form_id,qid='8')

            question_properties_8 = question_data_8
            question_properties_8['items'] = ''
            updated_question_8 = self.update_form_question_data(form_id,qid='8',question_properties=question_properties_8)
            
            response = {
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