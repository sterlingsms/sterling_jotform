from libs.jotform.jotform import *
from .jotform_api_base import JotformAPIBase
import json
import urllib
import urllib.parse
from datetime import datetime
from pytz import timezone, utc
import pytz

class MedicationLog(JotformAPIBase):
    def __init__(self, api_key, arg):
        JotformAPIBase.__init__(self, api_key, arg)

    def get_medication_log_form(self,form_id=None):
        medication_log_form_link = self.base_url + "/form/" + form_id + "/source?apiKey=" + self.api_key
        get_medication_log_form_source = urllib.request.urlopen(medication_log_form_link)
        medication_log_form_source = json.loads(get_medication_log_form_source.read())
        return medication_log_form_source

    def get_pst_time(self, date_format='%m/%d/%Y %H:%M:%S'):
        date = datetime.now(tz=pytz.utc)
        date = date.astimezone(timezone('US/Pacific'))
        pstDateTime = date.strftime(date_format)
        return pstDateTime

    def get_patient_medi_summary(self, patient_data):
        get_medi = json.loads(patient_data['answers']['151']['answer']);
        get_name = patient_data['answers']['45']['prettyFormat'];
        summary = get_name + ' has the following Daily Medicine Requirements:<br><br>';
        if len(get_medi) >= 1:
            for i in range(0, len(get_medi)):
                summary += '- ' + get_medi[i]['Number Taken Daily'] + ' x ' + get_medi[i]['Medication Name'] + ' (' + \
                           get_medi[i]['Dosage amount'] + ') | Prescribed by ' + get_medi[i][
                               'Ordering Doctor'] + ' since ' + get_medi[i]['Start Date'] + '<br>';
        return summary

    def get_log_table(self, medication_log=[], sid=None):
        takenTime = {
            "27": "Before breakfast",
            "28": "With breakfast",
            "29": "Before lunch",
            "30": "With lunch",
            "31": "Before dinner",
            "32": "With Dinner",
            "33": "Before bedtime",
            "34": "At bedtime",
            "41": "Medicaiton Refused"
        }
        getrow = ""
        gettabe = ""
        if len(medication_log) >= 1:
            for i in range(0, len(medication_log)):
                if medication_log[i]['answers']['51']['answer'] != sid:continue 
                getTaken = '';
                for x in medication_log[i]['answers']:
                    if x in takenTime and medication_log[i]['answers'][x].get('answer') is not None and \
                            medication_log[i]['answers'][x]['answer'] is not None:
                        getTaken += medication_log[i]['answers'][x]['answer'] + " (" + takenTime[x] + ")<br>"
                pstDateTime = self.pst_time(str(medication_log[i]['created_at']))
                #pstDateTime = medication_log[i]['created_at']  
                # datetime.strptime(str(medication_log[i]['created_at']),"%m/%d/%Y %H:%M:%S")
                getrow += "<tr><td>" + pstDateTime + "</td><td>" + medication_log[i]['answers']['35'][
                    'answer'] + "</td><td>" + medication_log[i]['answers']['36'][
                              'answer'] + "</td><td>" + getTaken + "</td></tr>"
        if getrow != '':
            gettabe = "<br><table><tr><th> Time Taken </th><th> Medication Name </th><th> Dosage Amount </th><th> " \
                      "Intake On </th></tr>" + getrow + "</table>"

        return gettabe

    def get_patient_medication_log(self,form_id,sid):
        # Patient sid - q51 in medication log form
        tdate = self.get_pst_time("%Y-%m-%d")  # datetime.today().strftime('%Y-%m-%d')
        submission_filter = {"51:eq": sid, "created_at:gt": tdate + " 00:00:00"}
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
        patient_data = self.get_submission_data(sid)
        medication_log_form_source = self.get_medication_log_form(form_id)
        get_summary = self.get_patient_medi_summary(patient_data)
        medication_log = self.get_patient_medication_log(form_id,sid)
        medication_log_table = self.get_log_table(medication_log,sid)
        # Patient name question id - q45
        get_name = patient_data['answers']['45']['prettyFormat'];
        # Medication Log question id - q151
        get_medi = json.loads(patient_data['answers']['151']['answer'])
        medication_name = []
        dosage_amount = []
        if len(get_medi) >= 1:
            for i in range(0, len(get_medi)):
                medication_name.append(get_medi[i]['Medication Name'])
                dosage_amount.append(get_medi[i]['Dosage amount'])

        response = {
            "name": get_name,
            "medication_name": medication_name,
            "dosage_amount": dosage_amount,
            "summary": get_summary,
            "medication_log": medication_log,
            "medication_log_table": medication_log_table,
            "medication_log_form_source": medication_log_form_source['content'],
            "tdate": self.get_pst_time('%Y-%m-%d')
        }
        return response